import os

class File():

    def __init__(self):
        self.__BASE_DIR_PATH = os.getcwd()
        self.__DATASET_DIR_PATH = os.path.join(self.__BASE_DIR_PATH, 'data')
    
    def getTrackData(self):
        filePath = os.path.join(self.__DATASET_DIR_PATH + '/track', 'case01.txt')

        with open(filePath, 'r') as dataSet:
            originData = dataSet.read().split('\n')
        
        startPoint = [0, 0]
        endArea = []
        trackData = []
        for index, data in enumerate(originData):
            temp = []
            for num in data.split(','):
                temp.append(int(num))

            if index == 0: startPoint = temp
            elif index <= 2: endArea.append(temp)
            else: trackData.append(temp)
        
        return (startPoint, endArea, trackData)

    def getAllFileUnderDirectory(self, filename):
        fileList = []
        for root, dirs, files in os.walk(self.__DATASET_DIR_PATH + '/track'):  
            for filename in files:
                fileList.append(filename)
        return fileList

    def getCarRecord(self, fName):
        filePath = os.path.join(self.__DATASET_DIR_PATH + '/record', fName)
        with open(filePath, 'r') as dataSet:
            originData = dataSet.read().split('\n')
        
        record = []
        for index, data in enumerate(originData):
            if data != '':
                temp = []
                num = data.split(' ')
                for num in data.split(' '):
                    temp.append(float(num))
                record.append(temp)
        return record

    def writeContentToFile(self, content, fName):
        with open(self.__DATASET_DIR_PATH + '/output/' + fName, 'w') as f:
            for point in content:
                if len(point) != 0:
                    pointStr = ''
                    for i in point[:len(point)-1]:
                        pointStr += str(i) + ' '
                    f.write(pointStr + str(point[len(point)-1]) + '\n')