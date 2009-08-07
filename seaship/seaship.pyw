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

class World2dCanvas(QWidget):
    def __init__(self, parent=None, world=None, painter=None):
        QtGui.QWidget.__init__(self, parent)
        if world is None:
            world = [[1]]
        self.world = world

        if painter is None:
            painter = QtGui.QPainter()
        self.painter = painter

    def paintEvent(self, event):
        self.draw_world2d(self.painter, self.world)
        self.update()

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
        if not painter.begin(self):
            print "failed."
            return
        if brush is None:
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            r, g, b, a = color
            brush.setColor(QtGui.QColor(r, g, b, a))
        painter.setBrush(brush)
        painter.drawRect(x*size, y*size, size, size)
        painter.end()

class SeashipMainWindow(QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # set up world
        self.random_world(width=10)

        # set up window
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Seaship')
        self.painter = QtGui.QPainter()
        
        self.worldcanvas = World2dCanvas(parent=self)
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.addWidget(self.worldcanvas)
        self.setCentralWidget(self.mainSplitter)
        
        # built tool bar
        # start button
        start_button = QtGui.QAction(QtGui.QIcon('icons/play.png'),
                'Start', self)
        start_button.setShortcut('Ctrl+R')
        start_button.setStatusTip('Start Planning')
        self.connect(start_button, QtCore.SIGNAL('triggered()'),
                self.plan)

        # stop button
        stop_button = QtGui.QAction(QtGui.QIcon('icons/stop.png'),
                'Start', self)
        stop_button.setShortcut('Ctrl+T')
        stop_button.setStatusTip('Stop')
        self.connect(stop_button, QtCore.SIGNAL('triggered()'),
                self.reset_world)

        reset_button = QtGui.QAction(QtGui.QIcon('icons/reset.png'),
                'Random', self)
        reset_button.setShortcut('Ctrl+N')
        reset_button.setStatusTip('Randomize World')
        self.connect(reset_button, QtCore.SIGNAL('triggered()'),
                self.random_world)

        toolbar = self.addToolBar('Control')
        toolbar.addAction(start_button)
        toolbar.addAction(stop_button)
        toolbar.addAction(reset_button)

        # status bar
        self.statusBar()

    def random_world(self, width=10):
        # set up world
        self.c = kapal.tools.rand_cost_map(width, width, 1, kapal.inf,
                flip=True, flip_chance=.1)
        self.c2 = copy.deepcopy(self.c)
        self.world = kapal.world.World2d(self.c, state_type = kapal.state.State2dAStar)

    def reset_world(self):
        self.c2 = copy.deepcopy(self.c)
        self.world.reset()

    def plan(self):
        # A* test
        def fake_h(s1, s2):
            return 0

        start_y = 2
        start_x = 2
        goal_y = 8
        goal_x = 8
        astar = kapal.algo.AStar(self.world, self.world.state(start_y,start_x),
                self.world.state(goal_y, goal_x))
        #astar.h = fake_h
        num_popped = 0
        for s in astar.plan_gen():
            if self.c2[s.y][s.x] < kapal.inf:
                self.c2[s.y][s.x] = -1
            num_popped += 1
        print num_popped
        for s in astar.path():
            self.c2[s.y][s.x] = -2

    def paintEvent(self, event):
        self.worldcanvas.world = copy.deepcopy(self.c2)
        self.update()

app = QtGui.QApplication(sys.argv)
seawin = SeashipMainWindow()
seawin.show()
app.exec_()
