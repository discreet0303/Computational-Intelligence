import pygame as pg
import tkinter as tk

class TrackLine(pg.sprite.Sprite):
    def __init__(self, color, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([38, 13])  #磚塊長寬38x13
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

class GameUI():
    def __init__(self):
        pg.init()

        #設定視窗
        width, height = 400, 400
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Sean's game")
        self.bg = pg.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((255,255,255))

        self.carCenterX = 100
        self.carCenterY = 350
        self.clock = pg.time.Clock()
        self.gameStart()

    def gameStart(self):
        self.drawCar()
        # self.drawTrack()
        allsprite = pg.sprite.Group()  #建立全部角色群組
        bricks = pg.sprite.Group()     #建立磚塊角色群組
        #建立磚塊
        for row in range(0, 5):          #5列方塊
            for column in range(0, 15):  #每列15磚塊
                if row == 1 or row == 0: 
                    brick = TrackLine((153,205,255), column * 40 + 1, row * 15 + 1)   #位置為40*15
                if row == 2: 
                    brick = TrackLine((94,175,254), column * 40 + 1, row * 15 + 1)    
                if row == 3 or row == 4:  
                    brick = TrackLine((52,153,207), column * 40 + 1, row * 15 + 1)  
                bricks.add(brick)     #加入磚塊角色群組
                allsprite.add(brick)  #加入全部角色群組


        running = True
        while running:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.carCenterY = self.carCenterY - 1
            self.carRect.center = (self.carCenterX, self.carCenterY)

            allsprite.draw(self.screen)  #繪製所有角色
            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.car, self.carRect.topleft)
            pg.display.update()
        pg.quit()

    def drawCar(self):
        self.car = pg.Surface((36, 36))
        self.car.fill((255,255,255))
        pg.draw.circle(self.car, (0,0,255), (18, 18), 18, 4)
        self.carRect = self.car.get_rect()
        self.carRect.center = (self.carCenterX, self.carCenterY)


    def drawTrack(self):
        startPositionX = 100
        startPositionY = 350
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
            if (index < len(data) - 1):
                pg.draw.line(
                    self.bg,
                    (0, 0, 255),
                    (startPositionX + point[0] * scale, startPositionY - point[1] * scale),
                    (startPositionX + data[index + 1][0] * scale, startPositionY - data[index + 1][1] * scale),
                    4
                )

          

GameUI()
