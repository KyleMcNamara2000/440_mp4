"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

import math

def getCounts(train):
    #I = map tag -> # times at start
    #T = map tagA -> dict(tagB, # times showed up after tagA)
    #E = map tag -> dict(word, # times tag made this word)
    I = {}
    T = {}
    E = {}
    oneTimers = {} #map once words -> their tags
    iCount = 0
    tCounts = {} #maps tagA -> totalCount
    eCounts = {} #maps tag -> totalCount
    for sentence in train:
        if sentence[0][0] in I:
            I[sentence[0][0]] += 1
        else:
            I[sentence[0][0]] = 1
        iCount += 1
        for i in range(len(sentence)):
            if i < len(sentence) - 1:
                if sentence[i][1] in T:
                    miniDict = T[sentence[i][1]]
                    if sentence[i + 1][1] in miniDict:
                        miniDict[sentence[i + 1][1]] += 1
                    else:
                        miniDict[sentence[i + 1][1]] = 1

                else:
                    T[sentence[i][1]] = {}
                    T[sentence[i][1]][sentence[i + 1][1]] = 1

                if sentence[i][1] in tCounts:
                    tCounts[sentence[i][1]] += 1
                else:
                    tCounts[sentence[i][1]] = 1

    for sentence in train:
        for pair in sentence:
            if pair[0] not in oneTimers:
                oneTimers[pair[0]] = pair[1]
            elif pair[0] in oneTimers:
                oneTimers.pop(pair[0])
            if pair[1] in E:
                miniDict = E[pair[1]]
                if pair[0] in miniDict:
                    miniDict[pair[0]] += 1
                else:
                    miniDict[pair[0]] = 1

            else:
                miniDict = {}
                miniDict[pair[0]] = 1
                E[pair[1]] = miniDict

            if pair[1] in eCounts:
                eCounts[pair[1]] += 1
            else:
                eCounts[pair[1]] = 1

    return I, T, E, iCount, tCounts, eCounts, oneTimers

'''
unnecessary fo da day
def getProbabilities(I, T, E, iCount, tCounts, eCounts):
    # I = map tag -> # times at start
    # T = map tagA -> dict(tagB, # times showed up before tagA)
    # E = map tag -> dict(word, # times tag made this word)
    #set START prob = 1
    for x in I:
        assert (iCount / I[x] == 1)
        I[x] = 1

    #update T's
    for tag, innerDict in T.items():
        for key in innerDict:
            #TODO: laplace?
            innerDict[key] = innerDict[key] / tCounts[tag]

    #update E's
    for tag, innerDict in E.items():
        for key in innerDict:
            innerDict[key] = innerDict[key] / eCounts[tag]

    return I, T, E
'''



def P_s(tag, internalMap, iCount, smoothing_parameter):
    for x in internalMap:
        if x == tag:
            return math.log(float(iCount + smoothing_parameter) / (iCount + smoothing_parameter * (iCount + 1)))
        else:
            return math.log((0.0 + smoothing_parameter) / (iCount + smoothing_parameter * (iCount + 1)))
    print("bad")
    return 0

#A=prev tag, B=curr tag
def P_t(tagA, tagB, transitionMap, tCounts, smoothing_parameter):
    if tagB in transitionMap[tagA]:
        return math.log(float(transitionMap[tagA][tagB] + smoothing_parameter) / (tCounts[tagA] + smoothing_parameter * (len(transitionMap[tagA]) + 1)))
    else:
        return math.log(float(0.0 + smoothing_parameter) / (tCounts[tagA] + smoothing_parameter * (len(transitionMap[tagA]) + 1)))

#p(WORD | TAG)
def P_e(word, tag, emissionMap, eCounts, smoothing_parameter, onesCount, oneTagCounts):
    #if tag in :
    #smoothing_parameter = smoothing_parameter * (oneTagCounts[tag] / onesCount)

    if word in emissionMap[tag]:
        return math.log(float(emissionMap[tag][word] + smoothing_parameter) / (eCounts[tag] + smoothing_parameter * (len(emissionMap[tag]) + 1)))
    else:
        if tag in oneTagCounts:
            smoothing_parameter = smoothing_parameter * (oneTagCounts[tag] / onesCount)
        else:
            smoothing_parameter = 1 * 10 ** -20
        return math.log(float(0.0 + smoothing_parameter) / (eCounts[tag] + smoothing_parameter * (len(emissionMap[tag]) + 1)))

def getUniqueTags(emissionMap):
    L = []
    S = set()
    for tag in emissionMap:
        if tag not in S:
            S.add(tag)
            L.append(tag)
    return L

def buildDaTrellis(internalMap, transitionMap, emissionMap, iCount, tCounts, eCounts, sentence, smoothing_parameter, onesCount, oneTagCounts):
    '''
    Initialization: We fill the first column using the initial probabilities. Specifically, the cell for tag t gets the value v(1,t)=PS(t)∗PE(w1∣t).

    Moving forwards in time: Use the values in column k to fill column k+1. Specifically
    For each tag tagB
    v(k+1,tagB)=maxtagA  v(k,tagA)∗PT(tagB∣tagA)∗PE(wk+1∣tagB)
    b(k+1,tagB)=argmaxtagA  v(k,tagA)∗PT(tagB∣tagA)∗PE(wk+1∣tagB)
    That is, we compute v(k,tagA)∗PT(tagB∣tagA)∗PE(wk+1∣tagB) for all possible tags tagA.
    The maximum value goes into trellis cell v(k+1,tagB) and the corresponding value of tagA is stored in b(k+1,tagB).

    Finishing: When we've filled the entire trellis, pick the best tag B in the final (time=n) column.
    Trace backwards from B, using the values in b, to produce the output tag sequence.
    '''
    uniqueTags = getUniqueTags(emissionMap)
    rows, cols = (len(sentence), len(uniqueTags))
    v = [[0 for i in range(cols)] for j in range(rows)]
    b = [["" for i in range(cols)] for j in range(rows)]
    for i in range(rows):
        for j in range(cols):
            tagB = uniqueTags[j]
            currWord = sentence[i]
            #print(currWord)
            # base case:
            if i == 0 and j == 0:
                v[i][j] = 0
            elif i == 0:
                v[i][j] = float('-inf')
                #v[i][j] = P_s(tagB, internalMap, iCount, smoothing_parameter) + P_e(currWord, tagB, emissionMap, eCounts, smoothing_parameter) #PS(t)∗PE(w1∣t)
            else:
                max = float('-inf')
                bestTag = None
                Ai = 0
                for tagA in uniqueTags:
                    if tagA != 'END':
                        oldV = v[i - 1][Ai]
                        curr = oldV + P_t(tagA, tagB, transitionMap, tCounts, smoothing_parameter) + P_e(currWord, tagB, emissionMap, eCounts, smoothing_parameter, onesCount, oneTagCounts)
                        if curr > max:
                            max = curr
                            bestTag = tagA
                    Ai += 1
                v[i][j] = max
                b[i][j] = bestTag
                #print("bt", bestTag)

    '''
    for i in range(rows):
        hey = ""
        for j in range(cols):
            hey += str(v[i][j]) + " " + str(b[i][j]) + ", "
        print(hey)
    print("\n\n\n\n\n")
    '''


    return v, b

'''
def getIndexOfTag(tagArr, tag):
    for i in range(len(tagArr)):
        if tagArr[i] == tag:
            return i
    print("uh ohhhhhhhhhhhhh")
    return -1
'''

#pick the best tag B in the final (time=n) column. Trace backwards from B, using the values in b, to produce the output tag sequence
def getPath(v, b, sentence, emissionMap):
    uniqueTags = getUniqueTags(emissionMap)
    rows, cols = (len(v), len(v[0]))
    path = []
    path.append((sentence[rows - 1], 'END'))

    #do last col calculation
    bestIndex = -1
    max = float('-inf')
    for j in range(cols):
        if v[rows - 1][j] > max:
            max = v[rows - 1][j]
            bestIndex = j

    #do middle calcs
    for i in range(rows - 2, 0, -1):
        path.append((sentence[i], b[i + 1][bestIndex]))
        bestIndex = uniqueTags.index(b[i + 1][bestIndex])

    #add start and reverse path
    path.append((sentence[0], 'START'))
    path.reverse()
    return path

    '''
    rows, cols = (len(sentence), len(getUniqueTags(emissionMap)))
    path = []
    path.append((sentence[rows - 1], 'END'))
    prev = None
    for ii in range(rows):
        i = rows - ii - 1
        if i == 0:
            path.append((sentence[i], 'START'))
        elif i == rows - 1:
            bestTag = None
            max = float('-inf')
            for j in range(cols):
                if v[i][j] > max:
                    max = v[i][j]
                    bestTag = b[i][j]
            #print("pair:", (sentence[i - 1], bestTag))
            path.append((sentence[i - 1], bestTag))
            prev = bestTag
        elif i > 1:
            #print("pair:", (sentence[i - 1], prev))
            path.append((sentence[i - 1], prev))
            prev = b[i][getIndexOfTag(b[i], prev)]

    path.reverse()
    return path
    '''


def workTags(oneTimers):
    oneTagCount = {} #tag -> count
    for word in oneTimers:
        tag = oneTimers[word]
        if tag in oneTagCount:
            oneTagCount[tag] += 1
        else:
            oneTagCount[tag] = 1
    return oneTagCount


def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # I = map tag -> # times at start
    # T = map tagA -> dict(tagB, # times showed up after tagA)
    # E = map tag -> dict(word, # times tag made this word)
    internalMap, transitionMap, emissionMap, iCount, tCounts, eCounts, oneTimers = getCounts(train)
    oneTagCounts = workTags(oneTimers)
    onesCount = len(oneTimers)
    output = []
    i = 0
    for sentence in test:
        v, b = buildDaTrellis(internalMap, transitionMap, emissionMap, iCount, tCounts, eCounts, sentence, 0.00001, onesCount, oneTagCounts)
        bestSequence = getPath(v, b, sentence, emissionMap)
        output.append(bestSequence)
        #if i > 0:
            #break
        i+=1
    '''
    for o in output:
        print(o)
    '''
    return output