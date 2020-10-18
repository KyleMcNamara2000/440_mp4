"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    #map word -> map tag -> # times
    wordDict = {}
    tagCounts = {} #map tag -> count
    for sentence in train:
        for pair in sentence:
            if pair[1] in tagCounts:
                tagCounts[pair[1]] += 1
            else:
                tagCounts[pair[1]] = 1
            if pair[0] in wordDict:
                miniDict = wordDict[pair[0]]
                if pair[1] in miniDict:
                    miniDict[pair[1]] += 1
                else:
                    miniDict[pair[1]] = 1
            else:
                miniDict = {}
                miniDict[pair[1]] = 1
                wordDict[pair[0]] = miniDict

    #get max num in dict
    overallTag = None
    overallNum = 0
    for tag, num in tagCounts.items():
        if num > overallNum:
            overallTag = tag
            overallNum = num

    output = [] #list of list of pairs
    for sentence in test:
        curr = []
        for word in sentence:
            if word in wordDict:
                miniDict = wordDict[word]
                maxTag = None
                maxNum = 0
                for tag, num in miniDict.items():
                    if num > maxNum:
                        maxTag = tag
                        maxNum = num
                curr.append((word, maxTag))
            else:
                curr.append((word, overallTag))
        output.append(curr)

    return output