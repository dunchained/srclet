import sys
import numpy as np
from screeninfo import get_monitors

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPalette, QColor

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# grid class
class Grid(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 120):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot()
        self.ax.set_ylim(-8.75, 8.75)
        self.ax.set_xlim(-8.75, 8.75)
        ticks = list(range(-8, 9))
        self.ax.xaxis.set_ticks(ticks)
        self.ax.yaxis.set_ticks(ticks)
        self.ax.grid(visible = True)
        self.ax.set_axisbelow(True)
        self.ax.tick_params(axis='both', which='both', length=0, labeltop=True, labelright=True)
        self.ax.set_aspect('equal')
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.title_font_ = {'fontsize': 16, 'fontweight': "normal", 'color': "black", 
                      'verticalalignment': "center", 'horizontalalignment': "center"}
        self.ax.set_title("Grid Title", fontdict = self.title_font_, pad = 35)
        self.circles = []
        super(Grid, self).__init__(fig)
    
    def createPattern(self, dots = 8, unified = True):
        self.dots = dots
        self.unified = unified
        # change title
        self.ax.set_title("Add Pattern", fontdict = self.title_font_, pad = 35)
        
        x = list(range(-8, -8+dots))
        y = [8.01]*dots
        
        if self.unified:
            coord = np.array(list(map(list, zip(x, y))))
            for i in range(self.pairs):
                circ = self.ax.add_patch(plt.Circle((coord[i,0], coord[i,1]), 0.35, color="royalblue"))
                self.circles.append(circ)
        else:
            xw = list(range(1, 1+dots))
            coord_blue = np.array(list(map(list, zip(x, y))))
            coord_pink = np.array(list(map(list, zip(xw, y))))
            for i in range(dots):
                circ = self.ax.add_patch(plt.Circle((coord_pink[i,0], coord_pink[i,1]), 0.35, color="deeppink"))
                self.circles.append(circ)
            for i in range(dots):
                circ = self.ax.add_patch(plt.Circle((coord_blue[i,0], coord_blue[i,1]), 0.35, color="deepskyblue"))
                self.circles.append(circ)
        # THIS IS NEW TO UPDATE THE PLOT
        self.draw()

class Side(QWidget):
    def __init__(self, color):
        super(Side, self).__init__()
        
        # background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        
        # add layout and text
        self.layout = QVBoxLayout()
        self.label = QLabel("Welcome to My first program")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
    def createPattern(self):
        # THIS IS NEW - THANK YOU MUSICAMENTE
        self.label.setText("Now we will create a pattern")

class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        screen = get_monitors()[0]
        self.setGeometry(int(screen.width*0.125), int(screen.height*0.125), 
                         int(screen.width*0.75), int(screen.height*0.75))
        self.setWindowTitle("My Program")
        self._createActions()
        self._createMenuBar()
        # THIS IS NEW TO PROPERLY CONNECT THE MENU ACTION
        self._connectActions()
        
        # a figure instance to plot on
        self.grid = Grid(width=8, height=8, dpi=140)
        # a side panel
        self.side = Side('white')
        
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout = QHBoxLayout(self.centralwidget)
        self.layout.addWidget(self.grid, 55)
        self.layout.addWidget(self.side, 45)
        
    def _createActions(self):
        self.newPatternAction = QAction("&New Pattern", self)
        
    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        patternMenu = menuBar.addMenu("&Pattern")
        patternMenu.addAction(self.newPatternAction)
        
    def _connectActions(self):
        self.newPatternAction.triggered.connect(self.newPattern)
    
    def newPattern(self):
        # Logic for creating a new file goes here...
        self.grid.createPattern()
        self.side.createPattern()

def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)    
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())