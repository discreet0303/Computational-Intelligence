import tkinter as tk
import time
import numpy as np
import math

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from src.algorithm.GeneAlgorithm import GeneAlgorithm
from src.algorithm.MathAlgorithm import MathAlgorithm
from src.car.Car import Car
from src.file.File import File

class Hw2Layout(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("790x480")
        self.title("Computer Intelligence - Gene & RBFN")
        self.runType = 0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.GeneAlgorithm = GeneAlgorithm()
        self.mathAlgorithm = MathAlgorithm()
        self.file = File()
        self.orbitData = [[], []]
        self.recordIndex = 0

        self.carStartInfo, self.endArea, self.track = self.file.getTrackData('case01.txt')
        self.car = Car(self.carStartInfo[:2], self.carStartInfo[2], self.ax, self.track, self.endArea)
        self.car.draw(False)

        self.componment()
        self.update()

    def update(self):
        if self.runType != 0:
            self.ax.clear()
            self.car.draw(True)

            if self.runType == 1:
                carState = self.car.updateCarPos()
                self.orbitData[0].append([
                    self.car.getSensorToTrackDistance('front'),
                    self.car.getSensorToTrackDistance('right'),
                    self.car.getSensorToTrackDistance('left'),
                    self.car.getcarSteeringWheelAngle(),
                ])
                self.orbitData[1].append([
                    self.car.carCenterPos[0],
                    self.car.carCenterPos[1],
                    self.car.getSensorToTrackDistance('front'),
                    self.car.getSensorToTrackDistance('right'),
                    self.car.getSensorToTrackDistance('left'),
                    self.car.getcarSteeringWheelAngle()
                ])
                
                if carState:
                    self.runType = 0
                else:
                    self.updateCarInfoLb()
                    fsDistance = self.car.getSensorToTrackDistance('front')
                    rsDistance = self.car.getSensorToTrackDistance('right')
                    lsDistance = self.car.getSensorToTrackDistance('left')
                    steeringWheelAngle = self.GeneAlgorithm.testing(fsDistance, rsDistance, lsDistance)
                    self.car.setcarSteeringWheelAngle(steeringWheelAngle)

                if self.runType == 0:
                    self.ax.clear()
                    self.car.draw(True)
                    self.updateCarInfoLb()
                    self.file.writeContentToFile(self.orbitData[0], 'train4D.txt')
                    self.file.writeContentToFile(self.orbitData[1], 'train6D.txt')
                    self.orbitData = [[], []]

            elif self.runType == 2:
                record4D = self.file.getCarRecord('train4D.txt')

                self.car.setcarSteeringWheelAngle(record4D[self.recordIndex][3])
                self.recordIndex += 1
                carState = self.car.updateCarPos()
                self.updateCarInfoLb()
                if carState: self.recordIndex = len(record4D)

                if len(record4D) == self.recordIndex:
                    self.runType = 0
                    self.recordIndex = 0

            elif self.runType == 3:
                record6D = self.file.getCarRecord('train6D.txt')

                self.car.setcarSteeringWheelAngle(record6D[self.recordIndex][5])
                self.recordIndex += 1
                carState = self.car.updateCarPos()
                self.updateCarInfoLb()
                if carState: self.recordIndex = len(record6D)

                if len(record6D) == self.recordIndex:
                    self.runType = 0
                    self.recordIndex = 0

            self.canvas.draw()
        self.after(100, self.update)

    def updateCarInfoLb(self):
        fsDistance = self.car.getSensorToTrackDistance('front')
        rsDistance = self.car.getSensorToTrackDistance('right')
        lsDistance = self.car.getSensorToTrackDistance('left')
        self.fsDistance_lb_var.set(fsDistance)
        self.rsDistance_lb_var.set(rsDistance)
        self.lsDistance_lb_var.set(lsDistance)
        self.carAngle_lb_var.set(self.car.getCarAngle())
        self.carSteeringWheelAngle_lb_var.set(round(self.car.getcarSteeringWheelAngle(), 4))

    def componment(self):
        plot_widget = self.canvas.get_tk_widget().place(x = 180, y = 0)

        genePos = (10, 0)
        self.algorithmSection_lb = tk.Label(self, text = 'Gene & RBFN 訓練', font = ('Arial', 12))
        self.algorithmSection_lb.place(x = genePos[0], y = genePos[1])
        self.start_training = tk.Button(self, text = "開始訓練", command = self.startTrain, width = 10, height = 1)
        self.start_training.place(x = genePos[0], y = genePos[1] + 25)

        self.data_vb_var = tk.StringVar()
        self.data_vb_var.set(1)
        self.data4D_lb = tk.Label(self, text = '訓練資料集', font = ('Arial', 10))
        self.data4D_lb.place(x = genePos[0], y = genePos[1] + 50)
        self.data4D_rb = tk.Radiobutton(self, text="4D", variable=self.data_vb_var, value=1)
        self.data4D_rb.place(x = genePos[0] + 70, y = genePos[1] + 50)
        self.data6D_rb = tk.Radiobutton(self, text="6D", variable=self.data_vb_var, value=2)
        self.data6D_rb.place(x = genePos[0] + 115, y = genePos[1] + 50)

        self.iterationTimes_lb = tk.Label(self, text = '迭代次數', font = ('Arial', 10))
        self.iterationTimes_lb.place(x = genePos[0], y = genePos[1] + 70)
        self.iterationTimes_lb_var = tk.StringVar()
        self.iterationTimes_lb_var.set('500')
        self.iterationTimes_tx = tk.Entry(self, width = 10, textvariable = self.iterationTimes_lb_var)
        self.iterationTimes_tx.place(x = genePos[0] + 70, y = genePos[1] + 70)

        self.genePoolSize_lb = tk.Label(self, text = '族群大小', font = ('Arial', 10))
        self.genePoolSize_lb.place(x = genePos[0], y = genePos[1] + 90)
        self.genePoolSize_lb_var = tk.StringVar()
        self.genePoolSize_lb_var.set('1000')
        self.genePoolSize_tx = tk.Entry(self, width = 10, textvariable = self.genePoolSize_lb_var)
        self.genePoolSize_tx.place(x = genePos[0] + 70, y = genePos[1] + 90)

        self.mating_lb = tk.Label(self, text = '交配機率', font = ('Arial', 10))
        self.mating_lb.place(x = genePos[0], y = genePos[1] + 110)
        self.mating_lb_var = tk.StringVar()
        self.mating_lb_var.set('0.6')
        self.mating_tx = tk.Entry(self, width = 10, textvariable = self.mating_lb_var)
        self.mating_tx.place(x = genePos[0] + 70, y = genePos[1] + 110)

        self.mutation_lb = tk.Label(self, text = '突變機率', font = ('Arial', 10))
        self.mutation_lb.place(x = genePos[0], y = genePos[1] + 130)
        self.mutation_lb_var = tk.StringVar()
        self.mutation_lb_var.set('0.01')
        self.mutation_tx = tk.Entry(self, width = 10, textvariable = self.mutation_lb_var)
        self.mutation_tx.place(x = genePos[0] + 70, y = genePos[1] + 130)

        infoPos = (10, 250)
        valueX = 100
        fileOptions = self.file.getAllTrackFilename()
        self.fileOptionValue = tk.StringVar('')
        self.fileOptionValue.set(fileOptions[0])

        self.carSection_lb = tk.Label(self, text = '自動車控制', font = ('Arial', 12))
        self.carSection_lb.place(x = infoPos[0], y = infoPos[1] - 90)

        self.start_bt = tk.Button(self, text = "開始測試", command = self.startBt, width = 10, height = 1)
        self.start_bt.place(x = infoPos[0], y = infoPos[1] - 65)

        self.fileOption_lb = tk.Label(self, text = '更換軌道', font = ('Arial', 10))
        self.fileOption_lb.place(x = infoPos[0], y = infoPos[1] - 35)

        self.fileOption_op = tk.OptionMenu(self, self.fileOptionValue, *fileOptions)
        self.fileOption_op.place(x = infoPos[0], y = infoPos[1] - 15)

        carAngle_tx = tk.Label(self, text = '自走車角度 :', font = ('Arial', 10))
        carAngle_tx.place(x = infoPos[0], y = infoPos[1] + 20)
        self.carAngle_lb_var = tk.StringVar()
        self.carAngle_lb_var.set(str(self.car.getCarAngle()))
        carAngle_lb = tk.Label(self, textvariable = self.carAngle_lb_var, font = ('Arial', 10))
        carAngle_lb.place(x = infoPos[0] + valueX, y = infoPos[1] + 20)

        carSteeringWheelAngle_tx = tk.Label(self, text = '方向盤角度 :', font = ('Arial', 10))
        carSteeringWheelAngle_tx.place(x = infoPos[0], y = infoPos[1] + 40)
        self.carSteeringWheelAngle_lb_var = tk.StringVar()
        self.carSteeringWheelAngle_lb_var.set(str(self.car.getcarSteeringWheelAngle()))
        carSteeringWheelAngle_lb = tk.Label(self, textvariable = self.carSteeringWheelAngle_lb_var, font = ('Arial', 10))
        carSteeringWheelAngle_lb.place(x = infoPos[0] + valueX, y = infoPos[1] + 40)

        fsDistance_tx = tk.Label(self, text = '前感測器距離 :', font = ('Arial', 10))
        fsDistance_tx.place(x = infoPos[0], y = infoPos[1] + 60)
        self.fsDistance_lb_var = tk.StringVar()
        self.fsDistance_lb_var.set(0)
        fsDistance_lb = tk.Label(self, textvariable = self.fsDistance_lb_var, font = ('Arial', 10))
        fsDistance_lb.place(x = infoPos[0] + valueX, y = infoPos[1] + 60)

        rsDistance_tx = tk.Label(self, text = '右感測器距離 :', font = ('Arial', 10))
        rsDistance_tx.place(x = infoPos[0], y = infoPos[1] + 80)
        self.rsDistance_lb_var = tk.StringVar()
        self.rsDistance_lb_var.set(0)
        rsDistance_lb = tk.Label(self, textvariable = self.rsDistance_lb_var, font = ('Arial', 10))
        rsDistance_lb.place(x = infoPos[0] + valueX, y = infoPos[1] + 80)

        lsDistance_tx = tk.Label(self, text = '左感測器距離 :', font = ('Arial', 10))
        lsDistance_tx.place(x = infoPos[0], y = infoPos[1] + 100)
        self.lsDistance_lb_var = tk.StringVar()
        self.lsDistance_lb_var.set(0)
        lsDistance_lb = tk.Label(self, textvariable = self.lsDistance_lb_var, font = ('Arial', 10))
        lsDistance_lb.place(x = infoPos[0] + valueX, y = infoPos[1] + 100)

        # self.readTrack_bt = tk.Button(self, text = "讀取 4D 記錄", command = self.readTrackBt, width = 15, height = 2)
        # self.readTrack_bt.place(x = infoPos[0], y = infoPos[1] + 150)
        # self.readHistory_bt = tk.Button(self, text = "讀取 6D 記錄", command = self.readHistoryBt, width = 15, height = 2)
        # self.readHistory_bt.place(x = infoPos[0], y = infoPos[1] + 200)
        
        self.loadDataSection_lb = tk.Label(self, text = '讀取檔案', font = ('Arial', 12))
        self.loadDataSection_lb.place(x = infoPos[0], y = infoPos[1] + 140)
        self.readHistory_bt = tk.Button(self, text = "讀取 RBFN 4D", command = self.readHistoryRBFN4D, width = 10, height = 1)
        self.readHistory_bt.place(x = infoPos[0], y = infoPos[1] + 165)

    def startBt(self):
        carStartInfo, endArea, track = self.file.getTrackData(self.fileOptionValue.get())
        self.car.resetCarState(carStartInfo[:2], carStartInfo[2])
        self.car.setTrack(track)
        self.car.setEndArea(endArea)
        self.runType = 1

    def readTrackBt(self):
        carStartInfo, endArea, track = self.file.getTrackData(self.fileOptionValue.get())
        self.car.resetCarState(carStartInfo[:2], carStartInfo[2])
        self.car.setTrack(track)
        self.car.setEndArea(endArea)
        self.runType = 2

    def readHistoryBt(self):
        carStartInfo, endArea, track = self.file.getTrackData(self.fileOptionValue.get())
        self.car.resetCarState(carStartInfo[:2], carStartInfo[2])
        self.car.setTrack(track)
        self.car.setEndArea(endArea)
        self.runType = 3
    
    def readHistoryRBFN4D(self):
        vector = self.file.getRBFNParam()
        self.GeneAlgorithm.loadRBFN(vector, 3)

    def startTrain(self):
        dimension = 3 if int(self.data_vb_var.get())  == 1 else 5
        iteration = int(self.iterationTimes_lb_var.get())
        genePoolSize = int(self.genePoolSize_lb_var.get())
        matingRate = float(self.mating_lb_var.get())
        mutationRate = float(self.mutation_lb_var.get())
        print(dimension)

        self.GeneAlgorithm.setGeneParam(dimension, genePoolSize, matingRate, mutationRate, 100000)
        for index in range(iteration):
            print('Iteration ', index)
            self.GeneAlgorithm.training()
        
        self.file.writeRBFNParamToFile(self.GeneAlgorithm.bestGene.vector)
