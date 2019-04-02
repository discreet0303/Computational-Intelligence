import os, sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
import time

scale = 6
startPosX = 200
startPosY = 350
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

scaleData = []
for index, point in enumerate(data[:-1]):
    scaleData.append([startPosX + point[0] * scale, startPosY - point[1] * scale])
print(scaleData)

def create_circle(x, y, r, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, width=3)

carCenterPosX = 200
carCenterPosY = 200
def drawCar(canvasObj):
    create_circle(carCenterPosX, carCenterPosY, 18, canvasObj)

def drawTrack(canvasObj):
    for index, point in enumerate(data[:-1]):
        startPos = (startPosX + point[0] * scale, startPosY - point[1] * scale)
        endPos = (startPosX + data[index + 1][0] * scale, startPosY - data[index + 1][1] * scale)
        canvasObj.create_line(startPos[0], startPos[1], endPos[0], endPos[1], fill="black", width=3)


master = tk.Tk()

w = tk.Canvas(master, width=500, height=500)
w.pack()

create_circle(100, 100, 20, w)
count = 0
while count < 100:
    count += 1
    w.delete("all")
    drawTrack(w)
    carCenterPosX += 1
    drawCar(w)
    w.update()
    time.sleep(0.03) 

tk.mainloop()


# # w.create_rectangle(50, 20, 150, 80, fill="#476042")
# # w.create_rectangle(65, 35, 135, 65, fill="yellow")
# # w.create_line(0, 0, 50, 20, fill="#476042", width=3)
# # w.create_line(0, 100, 50, 80, fill="#476042", width=3)
# # w.create_line(150,20, 200, 0, fill="#476042", width=3)
# # w.create_line(150, 80, 200, 100, fill="#476042", width=3)

# from tkinter import *
# import time
# gui = Tk()
# gui.geometry("800x800")
# c = Canvas(gui ,width=800 ,height=800)
# c.pack()
# oval = c.create_oval(5,5,60,60,fill='pink')
# xd = 5
# yd = 10
# while True:
#   c.move(oval,xd,yd)
#   p=c.coords(oval)
#   if p[3] >= 800 or p[1] <=0:
#      yd = -yd
#   if p[2] >=800 or p[0] <=0:
#      xd = -xd
#   gui.update()
#   time.sleep(0.025) 
# gui.title("First title")
# gui.mainloop()