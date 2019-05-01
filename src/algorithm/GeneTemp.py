import math
import random
import numpy as np

from src.algorithm.RBFN import RBFN
class Gene():

    def __init__(self):
        self.nNum = 8
        self.dimension = 3
        self.vectorLen = 1 + self.nNum + self.nNum * self.dimension + self.nNum
        self.vector = []

        self.RBFN = RBFN(self.nNum, self.dimension)

        self.randomBuild()

    def randomBuild(self):
        for index in range(self.vectorLen):
            if index == 0: self.vector.append(random.uniform(0, 1))
            elif index < 1 + self.nNum: self.vector.append(random.uniform(0, 1))
            elif index < 1 + self.nNum + self.nNum * self.dimension: self.vector.append(random.uniform(0, 1) * 30)
            else: self.vector.append(random.uniform(0, 1) * 10)
        
        self.vectorNormalization(self.vector)

    def getFitness(self, wheelValue, senValue):
        fitValue = 0
        for index, wheelAngle in enumerate(wheelValue):
            rbfnValue = self.RBFN.getOutput(senValue[index])
            fitValue += math.pow(wheelAngle - rbfnValue, 2)
        fitValue = fitValue / 2
        self.minFitValue = fitValue
        return fitValue
    
    def updateVector(self, vector):
        print('updateVector')
        self.vector = self.vectorNormalization(vector)

    def vectorNormalization(self, vector):
        for index in range(self.vectorLen):
            if index == 0: vector[index] = min(max(vector[index], 0), 1)
            elif index < 1 + self.nNum: vector[index] = min(max(vector[index], -40), 40)
            elif index < 1 + self.nNum + self.nNum * self.dimension: vector[index] = min(max(vector[index], 0), 30)
            else: vector[index] = min(max(vector[index], 0.000001), 10)
        
        self.RBFN.geneVectorTransform(vector)
        self.vector = vector
        return self.vector

    # def getFValue(self, senVector):
    #     value = 0
    #     for index in range(self.nNum):
    #         value += self.vector[index] * self.getGaussValue(senVector, index)
    #     return value

    # def getGaussValue(self, senVector, mIndex):
    #     mStartIndex = 1 + self.nNum + mIndex * self.dimension
    #     mEndIndex = 1 + self.nNum + (mIndex + 1) * self.dimension
    #     mValue = self.vector[mStartIndex:mEndIndex]
    #     sigmaValue = self.vector[1 + self.nNum + self.nNum * self.dimension + mIndex]
    #     # mValue = [1,1,1]
    #     # sigmaValue = 1

    #     value = np.array(senVector) - np.array(mValue)
    #     value = -np.sum(np.power(value, 2))

    #     return math.exp(value / (2 * sigmaValue ** 2))