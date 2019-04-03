import tkinter as tk
import time
import numpy as np
import math

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from src.algorithm.FuzzyAlgorithmHw1 import FuzzyAlgorithmHw1
from src.algorithm.MathAlgorithm import MathAlgorithm
from src.car.Car import Car

class Hw1Layout(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("840x480")
        self.runType = 0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.fuzzyAlgorithm = FuzzyAlgorithmHw1()
        self.mathAlgorithm = MathAlgorithm()

        self.track = [
            [-6, 0],
            [-6, 22],
            [18, 22],
            [18, 40],
            [30, 40],
            [30, 10],
            [6, 10],
            [6, 0],
            [-6, 0],
        ]
        self.car = Car([0, 0], 90, self.ax, self.track)
        self.car.draw(False)

        self.componment()
        self.update()

    def update(self):
        if self.runType != 0:
            self.ax.clear()
            self.car.draw(True)

            carState = self.car.updateCarPos()
            if carState: self.runType = 0

            fsDistance = self.car.getSensorToTrackDistance('front')
            rsDistance = self.car.getSensorToTrackDistance('right')
            lsDistance = self.car.getSensorToTrackDistance('left')
            self.fsDistance_lb_var.set(fsDistance)
            self.rsDistance_lb_var.set(rsDistance)
            self.lsDistance_lb_var.set(lsDistance)
            self.carSteeringWheelAngle_lb_var.set(self.car.getcarSteeringWheelAngle())

            steeringWheelAngle = self.fuzzyAlgorithm.fuzzySystem(fsDistance, rsDistance, lsDistance)
            self.car.setcarSteeringWheelAngle(steeringWheelAngle)

            # self.runType = 0
            self.canvas.draw()
        self.after(100, self.update)


    def componment(self):
        plot_widget = self.canvas.get_tk_widget().place(x = 200, y = 0)

        infoPos = (10, 40)
        valueX = 100
        self.start_bt = tk.Button(self, text = "開始", command = self.startBt, width = 15, height = 2)
        self.start_bt.place(x = 10, y = 10)

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


        self.readTrack_bt = tk.Button(self, text = "讀取軌道", command = self.readTrackBt, width = 15, height = 2)
        self.readTrack_bt.place(x = 0, y = 300)
        self.readHistory_bt = tk.Button(self, text = "讀取記錄", command = self.readHistoryBt, width = 15, height = 2)
        self.readHistory_bt.place(x = 10, y = 400)

    def startBt(self):
        self.car.setTrack(self.track)
        self.runType = 1
    def readTrackBt(self):
        self.runType = 2
    def readHistoryBt(self):
        self.runType = 3