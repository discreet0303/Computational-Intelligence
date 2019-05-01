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
        self.minFitness = 0

        self.RBFN = RBFN(self.nNum, self.dimension)
        self.randomBuild()

    def getFitness(self, wheelValue, senValue):
        fitValue = 0
        for index, wheelAngle in enumerate(wheelValue):
            rbfnValue = self.RBFN.getOutput(senValue[index])
            fitValue += math.pow(wheelAngle - rbfnValue, 2)
        fitValue = fitValue / 2
        self.minFitness = fitValue
        return self.minFitness

    def randomBuild(self):
        vector = []
        for index in range(self.vectorLen):
            if index == 0: vector.append(random.uniform(0, 1))
            elif index < 1 + self.nNum: vector.append(random.uniform(0, 1))
            elif index < 1 + self.nNum + self.nNum * self.dimension: vector.append(random.uniform(0, 1) * 30)
            else: vector.append(random.uniform(0, 1) * 10)

        self.updateVector(vector)

    def updateVector(self, vector):
        self.vector = vector
        self.RBFN.geneVectorTransform(vector)
