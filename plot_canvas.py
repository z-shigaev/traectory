import random
import time
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


class Layout(QVBoxLayout):
    def __init__(self, root, x, y):
        super().__init__()
        plt.style.use("classic")
        self.x = x
        self.y = y
        self.figure = plt.figure()
        self.ax = self.figure.add_axes([0.05, 0.1, 0.93, 0.85])
        self.ax.grid()
        self.ax.plot(x, y)
        self.canvas = FigureCanvas(self.figure)
        self.addWidget(self.canvas)

    def draw(self, x, y):
        self.figure.clear()
        self.ax = self.figure.add_axes([0.05, 0.1, 0.93, 0.85])
        # plt.gca().set_aspect('equal', adjustable='box')
        self.ax.grid()
        self.ax.plot(x, y)
        self.canvas.draw()
        # self.figure.clear()
        # self.ax = self.figure.add_axes([0.05, 0.1, 0.93, 0.85])
        # self.ax.grid()
        # self.ax.plot(x, y)
        # self.canvas.draw()