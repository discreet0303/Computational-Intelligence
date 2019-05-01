import numpy
import math

from src.algorithm.MathAlgorithm import MathAlgorithm

class RBFN():

    def __init__(self, nNum, dimension):
        self.nNum = nNum
        self.dimension = dimension

        self.theta = 0
        self.W = []
        self.M = []
        self.sigma = []

    def getOutput(self, x):
        output = self.theta
        for n in range(self.nNum):
            output += self.W[n] * math.exp(-1 * self.getHighDimVectorLength(x, self.M[n]) / (2 * self.sigma[n] * self.sigma[n]))
        return output 

    def geneVectorTransform(self, vector):
        self.theta = vector[0]
        self.W = vector[1:(self.nNum + 1)]
        temp = []
        for nIndex in range(self.nNum):
            startIndex = 1 + self.nNum + nIndex * self.dimension
            temp.append(vector[startIndex:(startIndex + self.dimension)])
        self.M = temp
        self.sigma = vector[(1 + self.nNum + self.nNum * self.dimension):]

    def getHighDimVectorLength(self, x, y):
        vLen = 0
        for index in range(len(x)):
            vLen += (x[index] - y[index]) ** 2
        return vLen