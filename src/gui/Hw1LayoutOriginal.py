import os, sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import time
import math
import numpy as np

from src.algorithm.FuzzyAlgorithmHw1 import FuzzyAlgorithmHw1

class Hw1Layout():
    def __init__(self, window):
        self.window = window
        self.window.title("Neural Network HW_01")
        self.window.resizable(0, 0)
        self.window.geometry("750x650+100+100")

        # init param
        self.startDrawPos = (200, 350)
        self.carCenterPos = [200, 350]
        self.carAngle = 90
        self.carSteeringWheelAngle = 0

        self.rightLinePox = 0
        self.frontLinePox = 0
        self.leftLinePox = 0

        self.scale = 6
        self.running = True
        self.trackData = [
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
        self.FuzzyAlgorithmHw1 = FuzzyAlgorithmHw1()
        self.mainCanvas = tk.Canvas(self.window, width=500, height=500)
        self.mainCanvas.pack()

        self.main()
        self.window.mainloop()

    def main(self):
        trackData = self.trackData
        count = 0
        while self.running:
            if count > 200: self.running = False
            count += 1
            self.mainCanvas.delete("all")

            self.drawTrack(trackData)
            self.drawCar()
            self.rightLineLength = self.getSersorDistance('right')
            self.frontLineLength = self.getSersorDistance('front')
            self.leftLineLength = self.getSersorDistance('left')

            if not self.checkAllTrackCollision():
                # if 30 < count < 100: self.carAngle -= 1
                
                # if count < 100 or count > 250:
                #     self.carCenterPos[1] -= 1
                # elif count < 250:
                #     self.carCenterPos[0] += 1
                self.updateCarPos()
                self.updateCarAngle()

                # self.carSteeringWheelAngle = self.FuzzyAlgorithmHw1.fuzzyAlgorithm(self.frontLineLength, self.rightLineLength, self.leftLineLength)
                self.carSteeringWheelAngle = 40
                # if count < 20:
                    # print('sensor len ========================')
                    # print(self.frontLineLength)
                    # print(self.rightLineLength)
                    # print(self.leftLineLength)
                    # print('car angle --------')
                    # print(self.carAngle)
                    # print(self.carSteeringWheelAngle)
                    # print(self.carCenterPos)

            self.mainCanvas.update()
            time.sleep(0.1) 

    def drawCar(self):
        carCenterPosX, carCenterPosY = self.carCenterPos
        self.create_circle(carCenterPosX, carCenterPosY, 18)
        self.rightLinePox = self.drawLineWithAngle(45)
        self.frontLinePox = self.drawLineWithAngle(0)
        self.leftLinePox = self.drawLineWithAngle(-45)


    def drawLineWithAngle(self, angle):
        carCenterPosX, carCenterPosY = self.carCenterPos
        angle = (self.carAngle - angle) * math.pi / 180.0
        endPosX = int(carCenterPosX + math.cos(angle) * 50)
        endPosY = int(carCenterPosY - math.sin(angle) * 50)
        self.mainCanvas.create_line(carCenterPosX, carCenterPosY, endPosX, endPosY, fill="black", width=3)
        return (endPosX, endPosY)

    def drawTrack(self, trackData):
        scale = self.scale
        startPosX, startPosY = self.startDrawPos
        for index, point in enumerate(trackData[:-1]):
            startPos = (startPosX + point[0] * scale, startPosY - point[1] * scale)
            endPos = (startPosX + trackData[index + 1][0] * scale, startPosY - trackData[index + 1][1] * scale)
            self.mainCanvas.create_line(startPos[0], startPos[1], endPos[0], endPos[1], fill="black", width=3)

    def create_circle(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.mainCanvas.create_oval(x0, y0, x1, y1, width=3)
    
    # update x, y, angle
    def updateCarPos(self):
        eqX1 = math.cos(math.radians(self.carAngle + self.carSteeringWheelAngle))
        eqX2 = math.sin(math.radians(self.carSteeringWheelAngle))
        eqX3 = math.sin(math.radians(self.carAngle))
        self.carCenterPos[0] = self.carCenterPos[0] + eqX1 + eqX2 * eqX3

        eqY1 = math.sin(math.radians(self.carAngle + self.carSteeringWheelAngle))
        eqY2 = math.sin(math.radians(self.carSteeringWheelAngle))
        eqY3 = math.cos(math.radians(self.carAngle))
        self.carCenterPos[1] = self.carCenterPos[1] - (eqY1 - eqY2 * eqY3)

    def updateCarAngle(self):
        self.carAngle = self.carAngle - math.degrees(math.asin(2 * math.sin(math.radians(self.carSteeringWheelAngle)) / 18))

    # get sensor length
    def getSersorDistance(self, sensorType):
        scaleTrack = []
        scale = self.scale
        startPosX, startPosY = self.startDrawPos
        trackData = self.trackData

        for p in trackData[:-1]:
            scaleTrack.append([startPosX + p[0] * scale, startPosY - p[1] * scale])
        
        lengths = []
        for index, point in enumerate(scaleTrack[:-1]):
            pointToTrack = self.getSensorToLineDistance(point, scaleTrack[index + 1], sensorType)
            if pointToTrack != 0:
                lengths.append(pointToTrack)
        if len(lengths) == 0: return 0
        return min(lengths)

    def getSensorToLineDistance(self, trackPoint1, trackPoint2, sensorType):
        sP1 = self.carCenterPos
        if sensorType == 'right':
            sP2 = self.rightLinePox
        elif sensorType == 'front':
            sP2 = self.frontLinePox
        if sensorType == 'left':
            sP2 = self.leftLinePox
        
        l1a, l1b, l1c = self.getLineWith2Point(trackPoint1, trackPoint2)
        l2a, l2b, l2c = self.getLineWith2Point(sP1, sP2)

        if l1b == 0 and l2b == 0:
            return 0
        elif l1b != 0 and l2b != 0:
            if l1a / l1b == l2a / l2b:
                return 0

        A = np.array([
            [l1a, l1b],
            [l2a, l2b]
        ])
        B = np.array([l1c, l2c]).reshape(2, 1)
        A_inv = np.linalg.inv(A)
        ans = A_inv.dot(B)
        pointWith2Line = (ans[0][0], ans[1][0])
        if self.getPointBetween2Point(trackPoint1, trackPoint2, pointWith2Line):
            sensorVector = np.array([pointWith2Line[0] - self.carCenterPos[0], pointWith2Line[1] - self.carCenterPos[1]])
            if sensorType != 'front':
                frontVector = np.array([self.frontLinePox[0] - self.carCenterPos[0], self.frontLinePox[1] - self.carCenterPos[1]])
            else:
                frontVector = np.array([self.rightLinePox[0] - self.carCenterPos[0], self.rightLinePox[1] - self.carCenterPos[1]])

            angle = np.dot(sensorVector, frontVector) / self.lineLength(sensorVector) / self.lineLength(frontVector)
            if 0 <= angle < 90:
                return self.lineLength(sensorVector)
            else:
                return 0
        return 0

    def getPointBetween2Point(self, trackPoint1, trackPoint2, point):
        if trackPoint1[0] <= point[0] <= trackPoint2[0] and trackPoint1[1] <= point[1] <= trackPoint2[1]:
            return True
        elif trackPoint1[0] <= point[0] <= trackPoint2[0] and trackPoint2[1] <= point[1] <= trackPoint1[1]:
            return True
        elif trackPoint2[0] <= point[0] <= trackPoint1[0] and trackPoint1[1] <= point[1] <= trackPoint2[1]:
            return True
        elif trackPoint2[0] <= point[0] <= trackPoint1[0] and trackPoint2[1] <= point[1] <= trackPoint1[1]:
            return True
        else:
            return False

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

    # track Collision detection
    def checkAllTrackCollision(self):
        scaleTrack = []
        scale = self.scale
        startPosX, startPosY = self.startDrawPos
        trackData = self.trackData

        for p in trackData[:-1]:
            scaleTrack.append([startPosX + p[0] * scale, startPosY - p[1] * scale])
        state = False
        for index, point in enumerate(scaleTrack[:-1]):
            # if index == 6:
            #     print(index)
            #     print(self.getCollisionToTrack(point, scaleTrack[index + 1], self.carCenterPos))
            if self.getCollisionToTrack(point, scaleTrack[index + 1], self.carCenterPos):
                state = True
        return state

    def getCollisionToTrack(self, point1, point2, center):
        trackVector = np.array(point2) - np.array(point1)
        centerVector = np.array(center) - np.array(point1)
        
        product = np.dot(trackVector, centerVector)
        angle = product / self.lineLength(trackVector) / self.lineLength(centerVector)

        distance = 0
        # if point1[0] == 236 and point1[1] == 290:
        #     print('getCollisionToTrack-----------')
        #     print(point1)
        #     print(trackVector)
        #     print(self.carCenterPos)
        #     print(centerVector)
        #     print(product)
        #     print(angle)
        if angle <= 0:
            distance = self.lineLength(centerVector)
        else:
            if product / self.lineLength(trackVector) > self.lineLength(trackVector):
                distance = self.lineLength(np.array(center) - np.array(point2))
            else:
                distance = math.sqrt(self.lineLength(centerVector) ** 2 - (product / self.lineLength(trackVector)) ** 2) / 2
        if distance < 18 / 2 + 1.5:
            return True
        return False

    def lineLength(self, point):
        return math.sqrt(point[0] ** 2 + point[1] ** 2)
