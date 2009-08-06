import sys
import PyQt4
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import kapal
import kapal.algo
import kapal.state
import kapal.world
import kapal.tools
import copy

class SeashipMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Seaship')
        self.painter = QtGui.QPainter()
        
        # A* test
        width = 10
        self.c = kapal.tools.rand_cost_map(width, width, 1, kapal.inf,
                flip=True, flip_chance=.0)
        self.c2 = copy.deepcopy(self.c)
        w = kapal.world.World2d(self.c, state_type = kapal.state.State2dAStar)

        start_y = 2
        start_x = 2
        goal_y = 8
        goal_x = 4
        astar = kapal.algo.AStar(w, w.state(start_y,start_x),
                w.state(goal_y, goal_x))
        num_popped = 0
        for s in astar.plan_gen():
            self.c2[s.y][s.x] = -1
            num_popped += 1
        print num_popped
        for s in astar.path():
            self.c2[s.y][s.x] = -2

    def paintEvent(self, event):
        self.draw_world2d(self.painter, self.c2)

    def draw_world2d(self, painter, world,
            x_start=0, y_start=0, x_goal=0, y_goal=0):
        for r in range(len(world)):
            for c in range(len(world[r])):
                color = (0, 80, 255, 255)       # blue
                if world[r][c] == -1:
                    color = (255, 0, 0, 255)    # red
                elif world[r][c] == -2:
                    color = (0, 255, 0, 255)    # green
                elif world[r][c] == kapal.inf:
                    color = (0, 0, 128, 255)       # blue
                self.draw_square(painter, c, r, color=color)

    def draw_square(self, painter, x=0, y=0, color=(0, 0, 0, 0), size=32, brush=None):
        painter.begin(self)
        if brush is None:
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            r, g, b, a = color
            brush.setColor(QtGui.QColor(r, g, b, a))
        painter.setBrush(brush)
        painter.drawRect(x*size, y*size, size, size)
        painter.end()

app = QtGui.QApplication(sys.argv)
seawin = SeashipMainWindow()
seawin.show()
app.exec_()
