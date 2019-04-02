import pygame as pg, random, math, time
import numpy as np

class GameUI():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500, 500))
        pg.display.set_caption("Sean's Brick Game")
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((255,255,255))

        self.originX = 200
        self.originY = 350
        self.carCenterX = 200
        self.carCenterY = 350

        self.allObjGroup = pg.sprite.Group()
        self.tracksGroup = pg.sprite.Group()
        self.arr = []
        self.createTrack()
        self.gameStart()

    def createTrack(self):
        scale = 7

        data = [
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

        index = 0
        for index, point in enumerate(data):
            if (index < len(data) - 2):
                self.arr.append((self.originX + point[0] * scale, self.originY - point[1] * scale))
            if (index < len(data) - 1):
                pg.draw.line(
                    self.bg,
                    (0, 0, 255),
                    (self.originX + point[0] * scale, self.originY - point[1] * scale),
                    (self.originX + data[index + 1][0] * scale, self.originY - data[index + 1][1] * scale),
                    4
                )
        self.screen.blit(self.bg, (0,0))
    
    def gameStart(self):
        self.drawCar()
        clock = pg.time.Clock()
        running = True

        while running:
            clock.tick(40)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            running = not self.checkCollisionToTrack([self.carCenterX, self.carCenterY])

            self.carCenterY = self.carCenterY - 1
            self.carRect.center = (self.carCenterX, self.carCenterY)
            self.newCar = pg.transform.rotate(self.car, 1)

            self.allObjGroup.draw(self.screen)
            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.newCar, self.carRect.topleft)
            pg.display.update()

        pg.quit()

    def drawCar(self):
        surfaceX = 60
        surfaceY = 100
        surfaceCenter = (int(surfaceX / 2), int(surfaceY / 2))
        # self.car = pg.Surface((surfaceX, surfaceY))
        self.car = pg.Surface((surfaceX, surfaceY), pg.SRCALPHA, 32)
        # self.car = self.car.convert_alpha()
        # self.car.fill((255,255,255))
        pg.draw.circle(self.car, (0,0,255), surfaceCenter, 21, 4)
        pg.draw.line(self.car, (0,0,255), surfaceCenter, (int(surfaceX / 2) - 30, int(surfaceY / 2) - 30), 6)
        pg.draw.line(self.car, (0,0,255), surfaceCenter, (int(surfaceX / 2) + 30, int(surfaceY / 2) - 30), 6)
        pg.draw.line(self.car, (0,0,255), surfaceCenter, (int(surfaceX / 2), int(surfaceY / 2) - 50), 4)
        self.carRect = self.car.get_rect()
        self.carRect.center = (self.carCenterX, self.carCenterY)



    def checkCollisionToTrack(self, carCenterPoint):
        state = False
        index = 0
        for index, point in enumerate(self.arr):
            if (index < len(self.arr) - 1):
                if self.getCollisionToTrack(point, self.arr[index + 1], carCenterPoint):
                    state = True
        return state

    def getCollisionToTrack(self, point1, point2, center):
        trackVector = np.array(point2) - np.array(point1)
        centerVector = np.array(center) - np.array(point1)
        
        product = np.dot(trackVector, centerVector)
        angle = product / self.lineLength(trackVector) / self.lineLength(centerVector)

        distance = 0
        if angle <= 0:
            distance = self.lineLength(centerVector)
            print('if')
        else:
            if product / self.lineLength(trackVector) > self.lineLength(trackVector):
                print('elseif')
                distance = self.lineLength(np.array(center) - np.array(point2))
            else:
                print('elseelse')
                distance = math.sqrt(self.lineLength(centerVector) ** 2 - (product / self.lineLength(trackVector)) ** 2) / 2

        if distance < 12:
            print(distance)
            return True
        return False

    def lineLength(self, point):
        return math.sqrt(point[0] ** 2 + point[1] ** 2)

GameUI()


# def getCollisionToTrack(point1, point2, center):
#     trackVector = np.array(point2) - np.array(point1)
#     centerVector = np.array(center) - np.array(point1)
    
#     product = np.dot(trackVector, centerVector)
#     angle = product / lineLength(trackVector) / lineLength(centerVector)

#     distance = 0
#     if angle <= 0:
#         distance = lineLength(centerVector)
#     else:
#         if product / lineLength(trackVector) > lineLength(trackVector):
#             print('elseif')
#             distance = lineLength(np.array(center) - np.array(point2))
#         else:
#             print('elseelse')
#             distance = math.sqrt(lineLength(centerVector) ** 2 - (product / lineLength(trackVector)) ** 2) / 2

#     print(angle)
#     print(distance)

# def lineLength(point):
#     return math.sqrt(point[0] ** 2 + point[1] ** 2)

# getCollisionToTrack((158,350), (158,196), (200,350))