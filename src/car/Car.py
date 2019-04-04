import math
import copy 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.algorithm.MathAlgorithm import MathAlgorithm

class Car():
    def __init__(self, startPoint, startAngle, ax, track, endArea):
        self.carCenterPos = startPoint
        self.carAngle = startAngle
        self.carRadius = 3
        self.carSteeringWheelAngle = 0

        self.mathAlgorithm = MathAlgorithm()
        
        self.fsPos = self.getSensorPos(0, 2)
        self.rsPos = self.getSensorPos(-45, 2)
        self.lsPos = self.getSensorPos(45, 2)

        self.ax = ax
        self.track = track
        self.carOrbit = [copy.deepcopy(self.carCenterPos)]
        self.endArea = endArea

        self.draw(False)

    def draw(self, drawSensor):
        # Track
        rect = patches.Rectangle(self.endArea[0] , self.endArea[1][0] - self.endArea[0][0], self.endArea[1][1] - self.endArea[0][1],linewidth=1,edgecolor='r',facecolor='none')
        self.ax.add_patch(rect)
        for index, line in enumerate(self.track[:-1]):
            self.ax.plot([line[0], self.track[index + 1][0]], [line[1], self.track[index + 1][1]], color='k',
                     linewidth=1, solid_capstyle='round')
        # Car
        car = plt.Circle(self.carCenterPos, 3, color='r',alpha=1)
        self.ax.add_artist(car)
        # Car orbit
        xOrbit = []
        yOrbit = []
        for point in self.carOrbit:
            xOrbit.append(point[0])
            yOrbit.append(point[1])
        self.ax.scatter(xOrbit, yOrbit, s=10, edgecolors='none', c='red')
        # Sensor
        if drawSensor:
            self.updateSensorPos()
            self.ax.plot([self.carCenterPos[0], self.fsPos[0]], [self.carCenterPos[1], self.fsPos[1]], linestyle='--', color='k', linewidth=1, solid_capstyle='round')
            self.ax.plot([self.carCenterPos[0], self.rsPos[0]], [self.carCenterPos[1], self.rsPos[1]], linestyle='--', color='k', linewidth=1, solid_capstyle='round')
            self.ax.plot([self.carCenterPos[0], self.lsPos[0]], [self.carCenterPos[1], self.lsPos[1]], linestyle='--', color='k', linewidth=1, solid_capstyle='round')

    def updateCarPos(self):
        eqX1 = round(math.cos(math.radians(self.carAngle + self.carSteeringWheelAngle)), 3)
        eqX2 = round(math.sin(math.radians(self.carSteeringWheelAngle)), 3)
        eqX3 = round(math.sin(math.radians(self.carAngle)), 3)
        self.carCenterPos[0] = round(self.carCenterPos[0] + eqX1 + eqX2 * eqX3, 3)

        eqY1 = round(math.sin(math.radians(self.carAngle + self.carSteeringWheelAngle)), 3)
        eqY2 = round(math.sin(math.radians(self.carSteeringWheelAngle)), 3)
        eqY3 = round(math.cos(math.radians(self.carAngle)), 3)
        self.carCenterPos[1] = round(self.carCenterPos[1] + eqY1 - eqY2 * eqY3, 3)

        self.carAngle = self.carAngle - int(math.degrees(math.asin(2 * math.sin(math.radians(self.carSteeringWheelAngle)) / (self.carRadius * 2))))
        self.carOrbit.append(copy.deepcopy(self.carCenterPos))
        isCarCollision = self.checkTrackCollision()
        return isCarCollision

    def updateSensorPos(self):
        self.fsPos = self.getSensorToTrackPos('front')
        self.rsPos = self.getSensorToTrackPos('right')
        self.lsPos = self.getSensorToTrackPos('left')

    def getSensorToTrackPos(self, sensorType):
        if sensorType == 'front': sPos = self.getSensorPos(0, 2)
        if sensorType == 'right': sPos = self.getSensorPos(-45, 2)
        if sensorType == 'left': sPos = self.getSensorPos(45, 2)

        sPosArr = []
        for trackIndex, point in enumerate(self.track[:-2]):
            crossPoint = self.mathAlgorithm.get2LineCrossPoint(point, self.track[trackIndex + 1], sPos, self.carCenterPos)
            if crossPoint != False:
                crossPoint = [round(crossPoint[0], 3), round(crossPoint[1], 3)]
                ansVector = np.array(crossPoint) - np.array(self.carCenterPos)
                sensorVector = np.array(sPos) - np.array(self.carCenterPos)
                product = np.dot(sensorVector, ansVector)
                cosValue = product / self.getVectorLength(sensorVector) / self.getVectorLength(ansVector)
                if cosValue > 0 and self.mathAlgorithm.checkPointBetween2Points(point, self.track[trackIndex + 1], crossPoint):
                    sPosArr.append(crossPoint)

        sPoslen = 100
        for point in sPosArr:
            if self.get2PointDistance(point, self.carCenterPos) < sPoslen:
                sPoslen = self.get2PointDistance(point, self.carCenterPos)
                sPos = point
        return sPos

    def checkTrackCollision(self):
        state = False
        if self.endArea[0][0] <= self.carCenterPos[0] <= self.endArea[1][0] and self.endArea[0][1] >= self.carCenterPos[1] >= self.endArea[1][1]:
            return True
        for index, point in enumerate(self.track[:-2]):
            if self.mathAlgorithm.getPointToLineDistance(point, self.track[index + 1], self.carCenterPos) < 3:
                state = True
        return state

    def getSensorPos(self, angle, scale):
        # L:angle > 0, R:angle < 0
        sensorAngle = self.carAngle + angle
        sensorEndPos = [
            round(self.carCenterPos[0] + math.cos(math.radians(sensorAngle)) * scale, 3),
            round(self.carCenterPos[1] + math.sin(math.radians(sensorAngle)) * scale, 3),
        ]
        return sensorEndPos

    def getSensorToTrackDistance(self, types):
        if types == 'front': return round(self.get2PointDistance(self.fsPos, self.carCenterPos), 3)
        if types == 'right': return round(self.get2PointDistance(self.rsPos, self.carCenterPos), 3)
        if types == 'left': return round(self.get2PointDistance(self.lsPos, self.carCenterPos), 3)

    def setTrack(self, trackData):
        self.track = trackData

    def setcarSteeringWheelAngle(self, angle):
        self.carSteeringWheelAngle = angle

    def getcarSteeringWheelAngle(self):
        return self.carSteeringWheelAngle

    def getCarAngle(self):
        return self.carAngle

    def setCarCenterPos(self, point):
        self.carCenterPos = point

    def getCarCenterPos(self):
        return self.carCenterPos

    def getVectorLength(self, vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def get2PointDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)