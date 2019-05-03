import math
import random
import copy
import numpy as np

from src.algorithm.Gene import Gene
from src.file.File import File

class GeneAlgorithm():
    
    def __init__(self):
        self.iteration = 500
        self.dimension = 3

        self.genePoolSize = 1000
        self.genePool = []
        self.minFitness = 10000
        self.matingRate = 0.6
        self.mutationRate = 0.01

        self.bestGene = None

        self.file = File()

    def training(self):
        for index in range(self.genePoolSize):
            if random.random() < self.matingRate:
                val = int(random.random() * (self.genePoolSize - 1))
                self.geneMating(self.genePool[index], self.genePool[val])

        for index in range(self.genePoolSize):
            if random.random() < self.mutationRate:
                self.geneMutation(self.genePool[index])

        self.getBestGene()

    def testingFor4D(self, fSen, rSen, lSen):
        return self.bestGene.RBFN.getOutput([fSen, rSen, lSen]) * 80 - 40

    def testingFor6D(self, x, y, fSen, rSen, lSen):
        return self.bestGene.RBFN.getOutput([x, y, fSen, rSen, lSen]) * 80 - 40
    
    def geneMating(self, geneA, geneB):
        sigmaVal = (random.random() - 0.5) * 2 * self.matingRate
        geneAVector = np.array(geneA.vector) + sigmaVal * (np.array(geneA.vector) - np.array(geneB.vector))
        geneBVector = np.array(geneB.vector) - sigmaVal * (np.array(geneA.vector) - np.array(geneB.vector))
        geneA.updateVector(geneAVector)
        geneB.updateVector(geneBVector)

    def geneMutation(self, gene):
        sigmaVal = (random.random() - 0.5) * 2 * self.mutationRate
        geneVector = np.array(gene.vector) + sigmaVal * random.random() * np.array(gene.vector)
        gene.updateVector(geneVector)

    def getBestGene(self):
        for geneIndex in range(self.genePoolSize):
            fit = self.genePool[geneIndex].getFitness(self.wheelRecord, self.senRecord)
            if fit < self.minFitness:
                self.minFitness = fit
                self.bestGene = copy.deepcopy(self.genePool[geneIndex])   
    
    def setGeneParam(self, dimension, genePoolSize, matingRate, mutationRate, minFitness):
        self.dimension = dimension
        self.genePoolSize = genePoolSize
        self.matingRate = matingRate
        self.mutationRate = mutationRate
        self.minFitness = minFitness

        fileName = 'train4D.txt' if self.dimension == 3 else 'train6D.txt'
        self.senRecord, self.wheelRecord = self.file.getCarRecordForGene(fileName)
        self.recordNormalization()

        self.genePool = []
        for size in range(self.genePoolSize):
            self.genePool.append(Gene(self.dimension))
    
    def recordNormalization(self):
        for index, wheel in enumerate(self.wheelRecord):
            self.wheelRecord[index] = (np.array(wheel) + 40) / 80

    def loadRBFN(self, vector, dataDimension):
        print('loadRBFN')
        self.bestGene = Gene(dataDimension)
        self.bestGene.updateVector(vector)

    # 4vector = [
    #     0.27413031070271554,-0.2165564702584432,0.43570801383368407,0.25766919736016813,0.8162115275208734,0.8162821060763124,0.8202941611263892,0.42819618155989114,0.08077460452911274,5.824353208226845,13.444845433520543,25.843555157662887,24.72074663331964,27.2452876319428,4.26792413219178,29.879182972982075,17.71580854125198,6.590448633825639,0.8439619974605179,25.090933045508315,15.210407312007572,26.40874256181456,25.714038156109435,29.958432120639543,0.3486954447339934,29.887137298021543,22.942949780787536,23.7447902299137,19.17562948615331,7.703035677504062,6.924410903031947,14.185147813621386,10.955673223625558,3.9415175026251936,9.477755884503381,0.2730688547204743,8.259032578761945,2.933900572696063,3.3994091470723804,9.982899337717233,1.196458072994222
    # ]

    # vector6d =[0.3314577730610375, 1.2183321081726128, 1.557934622746724, 0.3080828456782288, 0.7291432017815879, 1.2314183874778006, 2.155807295701578,0.39081250852022686, 0.7434143743221118, 0.008997195643978547,  1.7810518811343055,  9.383480543728732, 23.748940099019297, 10.043168670510601, 13.860769542424523, 24.46494545450288, 28.202942918756225, 24.877126793973563, 3.9222106689879697, 29.877963667569002, 28.396347719098557, 9.421677792657011, 11.162980712345448, 0.3468052347140606, 10.342886386409214, 24.974118896811085, 7.540382128022785, 1.0953311755495911, 29.998498548958363, 0.046913219247201376, 1.1011038377052575, 4.306768631106814, 29.998561290785688, 12.449489740729295, 1.927979889073564, 26.479774776775724, 0.5121427432301313, 22.80113107160742, 2.072223997473536, 0.004049267680546706, 0.006525454347247486, 29.938221316682128, 13.288957250131268, 8.925158752355541, 29.95244316597126, 3.4456902434559478, 0.2788639194474892, 14.472981799950828, 2.8857602683878203, 6.79775252348321, 9.998534643282436, 0.6543266933167925, 1.0037529895699917, 3.091226193327437, 9.985620674857863, 9.065722780560979, 9.016848732343306]