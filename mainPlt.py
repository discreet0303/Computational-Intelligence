import tkinter as tk
import time
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class SampleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.fig = Figure(figsize=(3,3), dpi=100)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.x =self.y=0
        self.ax.axis('equal')
        self.drawEdge()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        plot_widget = self.canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0)


        self.clock = tk.Label(self, text="")
        self.clock.grid(row=1, column=0)

        self.update_clock()

    def update_clock(self):
        self.ax.cla()
        self.drawEdge()
        self.y += 1

        self.canvas.draw()

        now = time.strftime("%H:%M:%S" , time.gmtime())
        self.clock.configure(text=now)
        self.after(100, self.update_clock)

    def drawEdge(self):
        c1 = plt.Circle((self.x, self.y), 3, color='r',alpha=1)
        self.ax.add_artist(c1)
        edge = [
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
        
        for index, line in enumerate(edge[:-1]):
            self.ax.plot((line[0], edge[index + 1][0]), (line[1], edge[index + 1][1]), 'k-')

if __name__== "__main__":
    app = SampleApp()
    app.mainloop()