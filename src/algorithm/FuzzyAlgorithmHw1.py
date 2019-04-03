import math
import numpy as np

class FuzzyAlgorithmHw1():
    def __init__(self):
        self.scale = 6
        self.ruleNum = 1

    def fuzzySystem(self, frontSensorLen, rightSensorLen, leftSensorLen):
        rulesWeight = [-40, 40]
        rules = [
            self.leftSensor(leftSensorLen, 'large'),
            self.rightSensor(rightSensorLen, 'large'),
        ]
        fuzzySum = 0
        rulesSum = 0
        for ruleNum, rule in enumerate(rules):
            fuzzySum += rule * rulesWeight[ruleNum]
            rulesSum += rule
        if rulesSum == 0:
            return 0
        elif fuzzySum / rulesSum < -40:
            return -40
        elif fuzzySum / rulesSum > 40:
            return 40
        return fuzzySum / rulesSum

    def frontSensor(self, frontDis, types):
        if types == 'small':
            if frontDis < 3:
                return 1
            elif frontDis < 10:
                return -frontDis / 7 + 10 / 7
            return 0
        elif types == 'medium':
            return 0
        elif types == 'large':
            if frontDis < 30:
                return 0
            return 1
        return 0

    def rightSensor(self, rightDis, types):
        if types == 'large':
            if rightDis < 8:
                return 0
            elif rightDis < 16:
                return rightDis / 6 - 8 / 6
            return 1
        return 0

    def leftSensor(self, leftDis, types):
        if types == 'large':
            if leftDis < 10:
                return 0
            elif leftDis < 16:
                return leftDis / 6 - 10 / 6
            return 1
        return 0