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
from src.car.Car import Car
# Hw1
if __name__== "__main__":
    app = Hw1Layout()
    app.mainloop()

    # a = FuzzyAlgorithmHw1()
    # a.fuzzyAlgorithmPPT(0,0,0)

    # a = Car([0,0], 90)

