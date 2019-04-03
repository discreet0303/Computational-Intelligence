import math
import numpy as np

class FuzzyAlgorithmHw1():
    def __init__(self):
        self.scale = 6
        self.ruleNum = 1

    def fuzzyAlgorithmPPT(self, frontSensorLen, rightSensorLen, leftSensorLen):
        rulesMinValue = []
        rulesCenterAveMethod = []
        for rule in range(0, self.ruleNum):
            minValue = np.array([self.frontSensorPPT(frontSensorLen, rule), self.rightLeftSensorPPT(rightSensorLen, leftSensorLen, rule)]).min() 
            rulesMinValue.append(minValue)
            rulesCenterAveMethod.append([])

        centerAveValue = 0
        for ruleIndex, rule in enumerate(rulesMinValue):

            for point in range(-100, 100):
                if rule >= self.carWheelAngle(point, ruleIndex) and self.carWheelAngle(point, ruleIndex) != 0:
                    rulesCenterAveMethod[ruleIndex].append(point)
            centerAveValue += np.array(rulesCenterAveMethod[ruleIndex]).sum() / len(rulesCenterAveMethod[ruleIndex]) * rule

        centerAveValue = centerAveValue / np.array(rulesMinValue).sum()
        # print(centerAveValue) 
        return centerAveValue

    def frontSensorPPT(self, frontSensorLen, ruleNum):
        if ruleNum == 0:
            # if 2 <= frontSensorLen <= 5:
            #     return (frontSensorLen - 2) / 3
            # elif 5 < frontSensorLen <= 8:
            #     return (8 - frontSensorLen) / 3
            return 0.5
        elif ruleNum == 1:
            if 3 <= frontSensorLen <= 6:
                return (frontSensorLen - 3) / 3
            elif 6 < frontSensorLen <= 9:
                return (9 - frontSensorLen) / 3
        return 0

    # def rightLeftSensorPPT(self, rightSensorLen, ruleNum):
        # rightLeftLen = rightSensorLen
    def rightLeftSensorPPT(self, rightSensorLen, leftSensorLen, ruleNum):
        rightLeftLen = rightSensorLen - leftSensorLen
        if ruleNum == 0:
            if rightLeftLen > 10 or rightLeftLen < -10:
                return 1
            elif rightLeftLen > 2 or rightLeftLen < -2:
                return (8 - rightLeftLen) / 6
            elif -2 < rightLeftLen < 2:
                return rightLeftLen / 4
            return 0
            # if 5 <= rightLeftLen <= 8:
            #     return (rightLeftLen - 5) / 3
            # elif 8 < rightLeftLen <= 11:
            #     return (11 - rightLeftLen) / 3
        elif ruleNum == 1:
            if 4 <= rightLeftLen <= 7:
                return (rightLeftLen - 4) / 3
            elif 7 < rightLeftLen <= 10:
                return (10 - rightLeftLen) / 3
        return 0

    def carWheelAngle(self, angle, ruleNum):
        if ruleNum == 0:
            if 1 <= angle <= 4:
                return (angle - 1) / 3
            elif 4 < angle <= 7:
                return (7 - angle) / 3
        elif  ruleNum == 1:
            if 3 <= angle <= 6:
                return (angle - 3) / 3
            elif 6 < angle <= 9:
                return (9 - angle) / 3
        return 0

    def fuzzyAlgorithm(self, frontSensorLen, rightSensorLen, leftSensorLen):
        roleToAngle = [0, 40, -40]

        # role 1
        role1 = []
        role1.append(self.frontSensor(frontSensorLen, 'large'))
        role1.append(self.rightLeftSensor(rightSensorLen, leftSensorLen, 'medium'))
        role1Score = min(role1)
        # role 2
        role2 = []
        role2.append(self.frontSensor(frontSensorLen, 'small'))
        role2.append(self.rightLeftSensor(rightSensorLen, leftSensorLen, 'small'))
        role2Score = min(role2)
        # role 3
        role3 = []
        role3.append(self.frontSensor(frontSensorLen, 'small'))
        role3.append(self.rightLeftSensor(rightSensorLen, leftSensorLen, 'large'))
        role3Score = min(role3)

        roleA = role1Score * roleToAngle[0] + role2Score * roleToAngle[1] + role3Score * roleToAngle[2]
        roleB = role1Score + role2Score + role3Score

        if roleB != 0:
            return roleA /roleB
        return 0

    def frontSensor(self, frontDistance, types):
        frontDistance = frontDistance / self.scale
        if types == 'large':
            if frontDistance < 36:
                return 0
            return 1
        elif types == 'medium':
            return 0
        elif types == 'small':
            if frontDistance < 12:
                return 1
            elif frontDistance < 24:
                return -0.5 * frontDistance + 3
        return 0

    def rightLeftSensor(self, rightDistance, leftDistance, types):
        distance = (rightDistance - leftDistance) / self.scale
        if types == 'large':
            if distance < 4:
                return 0
            elif distance < 5:
                return 5 - distance
            return 1
        elif types == 'medium':
            if distance > 0:
                return (5 - distance) / 5
            elif distance < 0:
                return (5 + distance) / 5
        elif types == 'small':
            if distance < -5:
                return 1
            elif distance < -4:
                return -4 - distance
            return 1

    def fuzzySystemGit(self, frontSensorLen, rightSensorLen, leftSensorLen):
        # rulesWeight = [55, 40, -55, -40, 60]
        rulesWeight = [40, -40]
        rules = [
            self.leftSensor(leftSensorLen, 'large'),
            self.rightSensor(rightSensorLen, 'large'),
        ]
        # print(leftSensorLen, rightSensorLen)
        # print(rules)
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

    def frontSensorGit(self, frontDis, types):
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
    # def frontSensorGit(self, frontDis, types):
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

    # def rightSensor(self, rightDis, types):
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

    # def leftSensor(self, leftDis, types):
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