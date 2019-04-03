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
class Hw1Layout(tk.Tk):
    def __init__(self):
        super().__init__()

        # car param
        self.carCenterPos = [0, 0]
        self.carAngle = 90
        self.carSteeringWheelAngle = 0
        # car sensor param
        self.frontLine = 0
        self.rightLine = 0
        self.leftLine = 0
        self.frontLinePox = [self.carCenterPos[0], self.carCenterPos[1] + 2]
        self.rightLinePox = [self.carCenterPos[0] + 2, self.carCenterPos[1] + 2]
        self.leftLinePox = [self.carCenterPos[0] - 2, self.carCenterPos[1] + 2]
        self.frontLineLength = 1
        self.rightLineLength = 1
        self.leftLineLength = 1
        # fuzzy init
        self.fuzzyAlgorithm = FuzzyAlgorithmHw1()
        # figure param
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('equal')

        # track param
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
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        plot_widget = self.canvas.get_tk_widget().grid(row=0, column=0)

        # init draw
        self.updateCanvas()
        self.update_clock()

    def update_clock(self):
        if not self.checkAllTrackCollision():
            print('carCenterPos Start')
            print(self.carCenterPos)
            print('carCenterPos End')
            self.ax.cla()
            self.updateCanvas()
            
            self.updateCarPos()
            self.updateCarAngle()

            self.frontLineLength = self.getSersorDistance('front')
            self.rightLineLength = self.getSersorDistance('right')
            self.leftLineLength = self.getSersorDistance('left')
            self.frontLinePox = [
                int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle - 0)) * self.frontLineLength),
                int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle - 0)) * self.frontLineLength)
            ]
            self.rightLinePox = [
                int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle - 45)) * self.rightLineLength),
                int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle - 45)) * self.rightLineLength)
            ]
            self.leftLinePox = [
                int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle + 45)) * self.leftLineLength),
                int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle + 45)) * self.leftLineLength)
            ]
            # self.carSteeringWheelAngle = 10
            self.carSteeringWheelAngle = -self.fuzzyAlgorithm.fuzzySystemGit(self.frontLineLength, self.rightLineLength, self.leftLineLength)
            print('self.carSteeringWheelAngle Start')
            print(self.carSteeringWheelAngle)
            print('self.carSteeringWheelAngle End')

            self.canvas.draw()
            
        self.after(100, self.update_clock)
        
        # self.frontLineLength = self.getSersorDistance('front')
        # # self.rightLineLength = self.getSersorDistance('right')
        # # self.leftLineLength = self.getSersorDistance('left')
        # # print('sensor length===')
        # print(self.frontLineLength)
        # # print(self.rightLineLength)
        # # print(self.leftLineLength)
        # # print(self.lineLength([8,8]))
        # self.frontLinePox = [
        #     int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle - 0)) * self.frontLineLength),
        #     int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle - 0)) * self.frontLineLength)
        # ]
        # # self.rightLinePox = [
        # #     int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle - 45)) * self.rightLineLength),
        # #     int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle - 45)) * self.rightLineLength)
        # # ]
        # # self.leftLinePox = [
        # #     int(self.carCenterPos[0] + math.cos(math.radians(self.carAngle + 45)) * self.leftLineLength),
        # #     int(self.carCenterPos[1] + math.sin(math.radians(self.carAngle + 45)) * self.leftLineLength)
        # # ]
        # # self.fuzzyAlgorithm.fuzzyAlgorithmPPT(4, 8, 0)
        # # self.fuzzyAlgorithm.fuzzyAlgorithmPPT(self.frontLineLength, self.rightLineLength, self.leftLineLength)
        # # a = self.fuzzyAlgorithm.fuzzySystemGit(self.frontLineLength, self.rightLineLength, self.leftLineLength)
        # # print(a)
        # # print(self.frontLineLength)
        # # print(self.rightLineLength)
        # # print(self.leftLineLength)
        # # self.checkAllTrackCollision()
        # self.ax.cla()
        # self.updateCanvas()
        # # self.after(1000, self.update_clock)

    def updateCanvas(self):
        # draw track
        for index, line in enumerate(self.track[:-1]):
            self.ax.plot((line[0], self.track[index + 1][0]), (line[1], self.track[index + 1][1]), 'k-')
        # draw sensor
        self.ax.plot((self.carCenterPos[0], self.frontLinePox[0]), (self.carCenterPos[1], self.frontLinePox[1]), 'k-')
        self.ax.plot((self.carCenterPos[0], self.rightLinePox[0]), (self.carCenterPos[1], self.rightLinePox[1]), 'k-')
        self.ax.plot((self.carCenterPos[0], self.leftLinePox[0]), (self.carCenterPos[1], self.leftLinePox[1]), 'k-')
        # drwa car
        car = plt.Circle(self.carCenterPos, 3, color='r',alpha=1)
        self.ax.add_artist(car)

    # update x, y, angle
    def updateCarPos(self):
        eqX1 = round(math.cos(math.radians(self.carAngle + self.carSteeringWheelAngle)), 3)
        eqX2 = round(math.sin(math.radians(self.carSteeringWheelAngle)), 3)
        eqX3 = round(math.sin(math.radians(self.carAngle)), 3)
        self.carCenterPos[0] = round(self.carCenterPos[0] + eqX1 + eqX2 * eqX3, 3)

        eqY1 = round(math.sin(math.radians(self.carAngle + self.carSteeringWheelAngle)), 3)
        eqY2 = round(math.sin(math.radians(self.carSteeringWheelAngle)), 3)
        eqY3 = round(math.cos(math.radians(self.carAngle)), 3)
        self.carCenterPos[1] = round(self.carCenterPos[1] + eqY1 - eqY2 * eqY3, 3)

    def updateCarAngle(self):
        self.carAngle = self.carAngle - int(math.degrees(math.asin(2 * math.sin(math.radians(self.carSteeringWheelAngle)) / 6)))

    def getSersorDistance(self, sensorType):
        sensorLenArr = []
        for trackIndex, point in enumerate(self.track[:-2]):
            sensorLen = self.getSensorToLineDistance(point, self.track[trackIndex + 1], sensorType)
            if sensorLen != 0: 
                sensorLenArr.append(sensorLen)
        if len(sensorLenArr) == 0: return 0
        return min(sensorLenArr)

    def getSensorToLineDistance(self, trackStartPos, trackEndPos, sensorType):
        carAngle = self.carAngle
        if sensorType == 'front': angle = carAngle
        elif sensorType == 'right': angle = carAngle - 45
        elif sensorType == 'left': angle = carAngle + 45

        sensorPos = [self.carCenterPos[0] + math.cos(math.radians(angle)) * 2, self.carCenterPos[1] + math.sin(math.radians(angle)) * 2]
        sensorEq = self.getLineWith2Point(self.carCenterPos, sensorPos)
        trackEq = self.getLineWith2Point(trackStartPos, trackEndPos)

        eq_axby = np.array([sensorEq[:2], trackEq[:2]])
        eq_c = np.array([sensorEq[2], trackEq[2]]).reshape(2, 1)
        eq_det = np.linalg.det(eq_axby)

        if eq_det == 0: return 0
        ans = np.linalg.solve(eq_axby, eq_c)
        ans = [ans[0][0], ans[1][0]]
        sensorVector = np.array(sensorPos) - np.array(self.carCenterPos)
        ansVector = np.array(ans) - np.array(self.carCenterPos)
        product = np.dot(sensorVector, ansVector)
        cosValue = product / self.lineLength(sensorVector) / self.lineLength(ansVector)

        if cosValue < 0: return 0
        if not self.checkPointBetween2Points(trackStartPos, trackEndPos, ans): return 0
        return self.lineLength(ansVector)

    def getLineWith2Point(self, point1, point2):
        # ax + by = c
        a = 0
        b = 0
        c = 0
        if point1[0] == point2[0]:
            a = 1
            c = point1[0]
        elif point1[1] == point2[1]:
            b = 1
            c = point1[1]
        else:
            a = (point1[1] - point2[1]) / (point1[0] - point2[0])
            b = -1
            c = a * point1[0] + b * point1[1]

        return (a, b, c)

    # track collision detection
    def checkAllTrackCollision(self):
        trackData = self.track
        state = False
        for index, point in enumerate(trackData[:-2]):
            if self.getCollisionToTrack(point, trackData[index + 1], self.carCenterPos):
                state = True
        return state

    def getCollisionToTrack(self, trackStartPos, trackEndPos, carCenterPos):
        if self.checkPointBetween2Points(trackStartPos, trackEndPos, carCenterPos):
            trackVector = np.array(trackEndPos) - np.array(trackStartPos)
            centerVector = np.array(carCenterPos) - np.array(trackStartPos)
            product = np.dot(trackVector, centerVector)
            cosValue = product / self.lineLength(trackVector) / self.lineLength(centerVector)
        else:
            carToStartPos = np.array(carCenterPos) - np.array(trackStartPos)
            carToEndPos = np.array(carCenterPos) - np.array(trackEndPos)

            if self.lineLength(carToStartPos) > self.lineLength(carToEndPos):
                trackVector = np.array(trackStartPos) - np.array(trackEndPos)
                centerVector = np.array(carCenterPos) - np.array(trackEndPos)
            else:
                trackVector = np.array(trackEndPos) - np.array(trackStartPos)
                centerVector = np.array(carCenterPos) - np.array(trackStartPos)

            product = np.dot(trackVector, centerVector)
            cosValue = product / self.lineLength(trackVector) / self.lineLength(centerVector)

        distance = 0
        if product == 0:
            distance = self.lineLength(centerVector)
        else:
            sinValue = math.sqrt(1 - cosValue ** 2)
            verticalDistance = sinValue * self.lineLength(centerVector)
            if cosValue < 0:
                distance = self.lineLength(centerVector)
            else:
                distance = verticalDistance
        if distance < 3.5:
            return True
        return False

    def checkPointBetween2Points(self, point1, point2, carCenterPos):
        if point1[0] == point2[0]:
            if point1[1] < carCenterPos[1] < point2[1]:
                return True
            elif point1[1] > carCenterPos[1] > point2[1]:
                return True
        elif point1[1] == point2[1]:
            if point1[0] < carCenterPos[0] < point2[0]:
                return True
            elif point1[0] > carCenterPos[0] > point2[0]:
                return True
        elif point1[0] < carCenterPos[0] < point2[0]:
            if point1[1] == point2[1]:
                return True 
            elif point1[1] < carCenterPos[1] < point2[1]:
                return True
            elif point1[1] > carCenterPos[1] > point2[1]:
                return True
        elif point1[0] < carCenterPos[0] < point2[0]:
            if point1[1] == point2[1]:
                return True 
            elif point1[1] < carCenterPos[1] < point2[1]:
                return True
            elif point1[1] > carCenterPos[1] > point2[1]:
                return True
        return False

    def lineLength(self, point):
        return math.sqrt(point[0] ** 2 + point[1] ** 2)