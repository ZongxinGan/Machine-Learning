__author__ = 'wsjswy'


from  numpy import  *

import math
import  feedparser

def loadDataSet():
        postingList = [
            ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
            ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
            ['my', 'dalmation', 'is', 'so', 'cute','I', 'love', 'him'],
            ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
            ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
            ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
        ]

        classVec = [0, 1, 0, 1, 0, 1]

        return  postingList, classVec

def  createVocabList(dataSet):
        vocabSet = set([])

        for document in dataSet:
            vocabSet = vocabSet | set(document)

        return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):

    returnVec = [0] * len(vocabList)

    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)

    return returnVec

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    p1Vect = p1Num / p1Denom
    p0Vect = p0Num / p0Denom

    return p0Vect, p1Vect, pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return  1
    else:
        return  0


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []

    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))

    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))


    #测试数据 1
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    #
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))

    print(testEntry, 'calssified as: ', classifyNB(thisDoc, p0V, p1V, pAb))


def calcMostFreq(vocabList, fullText):
    freqDict = {}

    for token in vocabList:
        freqDict[token] = fullText.count(token)

    sortedFreq = sorted(freqDict.items(), key = operator.itemgetter(1), reverse = True)

    return sortedFreq[:30]



def localWords(feed0, feed1):

    docList = []; classList = []; fullText = []

    minLen = min(len(feed1['entries']), len(feed0['entries']))

    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)

    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2 * minLen)
    testSet = []
    for i in range(20):
        randIndex = int(random.unform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []
    trainClasses = []

    for docIndex in trainingSet:
        #trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])



def testFun():
    mySent = 'what a stupid boy'

    print(mySent.split())


def textParse(bigString):
    listofTokens = re.split(r'\W*', bigString)

    return [tok.lower() for tok in listofTokens if len(tok) > 2]


if __name__ == "__main__":

    # listOPosts, listClasses = loadDataSet()
    #
    # myVocabList = createVocabList(listOPosts)
    #
    # print(myVocabList)
    #
    # print(setOfWords2Vec(myVocabList, listOPosts[0]))

    testFun()