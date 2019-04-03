import math
import numpy as np

class MathAlgorithm():
    # def __init__():
    #     self.test = 0

    def checkPointBetween2Points(self, point1, point2, centerPoint):
        if point1[0] == point2[0] or point1[1] == point2[1]:
            if point1[0] < centerPoint[0] < point2[0] or point1[0] > centerPoint[0] > point2[0]:
                return True
            elif point1[1] < centerPoint[1] < point2[1] or point1[1] > centerPoint[1] > point2[1]:
                return True
        elif point1[0] < centerPoint[0] < point2[0] or point1[0] > centerPoint[0] > point2[0]:
            if point1[1] == point2[1] or point1[1] < centerPoint[1] < point2[1] or point1[1] > centerPoint[1] > point2[1]:
                return True

        return False

    def get2PointsToLine(self, point1, point2):
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
        return [a, b, c]

    def get2LineCrossPoint(self, line1Point1, line1Point2, line2Point1, line2Point2):
        line1Eq = self.get2PointsToLine(line1Point1, line1Point2)
        line2Eq = self.get2PointsToLine(line2Point1, line2Point2)

        eq_axby = np.array([line1Eq[:2], line2Eq[:2]])
        eq_c = np.array([line1Eq[2], line2Eq[2]]).reshape(2, 1)
        eq_det = np.linalg.det(eq_axby)

        if eq_det == 0: return False
        ans = np.linalg.solve(eq_axby, eq_c)
        ans = [ans[0][0], ans[1][0]]

        return ans

    def getPointToLineDistance(self, lineStartPos, lineEndPos, centerPoint):
        if self.checkPointBetween2Points(lineStartPos, lineEndPos, centerPoint):
            lineVector = np.array(lineEndPos) - np.array(lineStartPos)
            pointVector = np.array(centerPoint) - np.array(lineStartPos)
        else:
            if self.get2PointDistance(lineStartPos, centerPoint) < self.get2PointDistance(lineEndPos, centerPoint):
                lineVector = np.array(lineEndPos) - np.array(lineStartPos)
                pointVector = np.array(centerPoint) - np.array(lineStartPos)
            else:
                lineVector = np.array(lineStartPos) - np.array(lineEndPos)
                pointVector = np.array(centerPoint) - np.array(lineEndPos)

        distance = 0
        product = np.dot(lineVector, pointVector)
        if product == 0: distance = self.getVectorLength(pointVector)

        cosValue = product / self.getVectorLength(lineVector) / self.getVectorLength(pointVector)
        if cosValue < 0: distance = self.getVectorLength(pointVector)
        else:
            sinValue = math.sqrt(1 - cosValue ** 2)
            distance = sinValue * self.getVectorLength(pointVector)
        return distance

    def getVectorLength(self, vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def get2PointDistance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

