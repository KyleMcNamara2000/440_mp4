"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

def getCounts(train):
    #I = map tag -> # times at start
    #T = map tagA -> dict(tagB, # times showed up before tagA)
    #E = map tag -> dict(word, # times tag made this word)
    I = {}
    T = {}
    E = {}
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
            if i > 0:
                if sentence[i][1] in T:
                    miniDict = T[sentence[i][1]]
                    if sentence[i - 1][1] in miniDict:
                        miniDict[sentence[i - 1][1]] += 1
                    else:
                        miniDict[sentence[i - 1][1]] = 1

                    if sentence[i][1] in tCounts:
                        tCounts[sentence[i][1]] += 1
                    else:
                        tCounts[sentence[i][1]] = 1
                else:
                    T[sentence[i][1]] = {}
                    T[sentence[i][1]][sentence[i - 1][1]] = 1

                    if sentence[i][1] in tCounts:
                        tCounts[sentence[i][1]] += 1
                    else:
                        tCounts[sentence[i][1]] = 1

    for sentence in train:
        for pair in sentence:
            if pair[1] in E:
                miniDict = E[pair[1]]
                if pair[0] in miniDict:
                    miniDict[pair[0]] += 1
                else:
                    miniDict[pair[0]] = 1

                if pair[1] in eCounts:
                    eCounts[pair[1]] += 1
                else:
                    eCounts[pair[1]] = 1
            else:
                miniDict = {}
                miniDict[pair[0]] = 1
                E[pair[1]] = miniDict

                if pair[1] in eCounts:
                    eCounts[pair[1]] += 1
                else:
                    eCounts[pair[1]] = 1

    return I, T, E, iCount, tCounts, eCounts

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





def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # I = map tag -> # times at start
    # T = map tagA -> dict(tagB, # times showed up before tagA)
    # E = map tag -> dict(word, # times tag made this word)
    internalMap, transitionMap, emissionMap, iCount, tCounts, eCounts = getCounts(train)

    return []