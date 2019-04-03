# def calcu(frontSensorLen, rightSensorLen, leftSensorLen):
#     rulesWeight = [55, -55, -40, 40, 60]
#     rules = [
#         leftSensor(leftSensorLen, 'large'),
#         rightSensor(rightSensorLen, 'large'),
#         rightSensor(rightSensorLen, 'medium'),
#         leftSensor(leftSensorLen, 'medium'),
#         frontSensor(frontSensorLen, 'small'),
#     ]

#     fuzzySum = 0
#     for ruleNum, rule in enumerate(rulesWeight):
#         fuzzySum += rule * rulesWeight[ruleNum]

#     return fuzzySum / rules.sum()

# def frontSensor(frontDis, types):
#     if types == 'small':
#         if frontDis < 3:
#             return 1
#         elif frontDis < 10:
#             return -frontDis / 7 + 10 / 7
#         return 0
#     elif types == 'medium':
#         return 0
#     elif types == 'large':
#         if frontDis < 30:
#             return 0
#         return 1
#     return 0

# def rightSensor(rightDis, types):
#     if types == 'small':
#         if rightDis < 4:
#             return 1
#         elif rightDis < 5:
#             return -rightDis + 5
#         return 0
#     elif types == 'medium':
#         if rightDis < 4:
#             return 0
#         elif rightDis < 10:
#             return rightDis / 6 - 4 / 6
#         elif rightDis < 16:
#             return rightDis / 6 + 16 / 6
#         return 0
#     elif types == 'large':
#         if rightDis < 8:
#             return 0
#         elif rightDis < 16:
#             return rightDis / 8 - 1
#     return 0

# def leftSensor(leftDis, types):
#     if types == 'small':
#         if leftDis < 4:
#             return 1
#         elif leftDis < 5:
#             return -leftDis + 5
#         return 0
#     elif types == 'medium':
#         if leftDis < 4:
#             return 0
#         elif leftDis < 10:
#             return leftDis / 6 - 4 / 6
#         elif leftDis < 16:
#             return -leftDis / 6 + 16 / 6
#         return 0
#     elif types == 'large':
#         if leftDis < 10:
#             return 0
#         elif leftDis < 16:
#             return leftDis / 6 - 10 / 6
#         return 1
#     return 0

import os, sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import numpy as np
import math

from src.gui.Hw1Layout import Hw1Layout

# Hw1
def getSersorDistance(sensorType):

    sensorLenArr = []
    for trackIndex, point in enumerate(track[:-2]):
        sensorLen = getSensorToLineDistance(point, track[trackIndex + 1], sensorType)
        if sensorLen != 0: sensorLenArr.append(sensorLen)

    if len(sensorLenArr) == 0: return 0
    return min(sensorLenArr)

def getSensorToLineDistance(trackStartPos, trackEndPos, sensorType):
    carAngle = 0
    if sensorType == 'front': angle = carAngle
    elif sensorType == 'right': angle = carAngle - 45
    elif sensorType == 'left': angle = carAngle + 45

    sensorPos = [ 10 + math.cos(math.radians(angle)) * 5, 18 + math.sin(math.radians(angle)) * 5]
    sensorEq = getLineWith2Point([10, 18], sensorPos)
    trackEq = getLineWith2Point(trackStartPos, trackEndPos)

    eq_axby = np.array([sensorEq[:2], trackEq[:2]])
    eq_c = np.array([sensorEq[2], trackEq[2]]).reshape(2, 1)
    eq_det = np.linalg.det(eq_axby)

    if eq_det == 0: return [10, 18]
    ans = np.linalg.solve(eq_axby, eq_c)
    ans = [ans[0][0], ans[1][0]]

    sensorVector = np.array(sensorPos) - np.array([10, 18])
    ansVector = np.array(ans) - np.array([10, 18])
    product = np.dot(sensorVector, ansVector)
    cosValue = product / lineLength(sensorVector) / lineLength(ansVector)

    if cosValue < 0: return 0
    return lineLength(ansVector)


def getLineWith2Point(point1, point2):
        # ax + by = c
        a = b = c =0
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

def lineLength(point1):
    return math.sqrt((point1[0]) ** 2 + (point1[1]) ** 2)

if __name__== "__main__":
    app = Hw1Layout()
    app.mainloop()

    # a = FuzzyAlgorithmHw1()
    # a.fuzzyAlgorithmPPT(0,0,0)

    # 10, 18
    # getSersorDistance('right')
    # print(getSensorToLineDistance([30, 10],[6, 10], 'right'))
