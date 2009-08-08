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
    world_list = ["2d 4 neighbors", "2d 8 neighbors"]
    algo_list = ["Dijkstra", "A*"]
    heuristic_list = ["Manhattan", "Euclidean"]

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # general settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up planner
        self.algo_t = kapal.algo.Dijkstra
        self.world_t = kapal.world.World2d
        self.state_t = kapal.state.State2dAStar
        self.random_world(width=10)

        # set up window
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Seaship')
        self.painter = QtGui.QPainter()

        # world canvas
        self.worldcanvas = World2dCanvas(parent=self)
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainSplitter.addWidget(self.worldcanvas)
        
        # world chooser
        self.world_combo = QtGui.QComboBox()
        self.world_combo.addItems(SeashipMainWindow.world_list)
        self.world_combo.setItemIcon(0, QtGui.QIcon('icons/2d_4neigh.png'))
        self.world_combo.setItemIcon(1, QtGui.QIcon('icons/2d_8neigh.png'))

        # algorithm chooser
        self.algo_combo = QtGui.QComboBox()
        self.algo_combo.addItems(SeashipMainWindow.algo_list)
        self.connect(self.algo_combo, SIGNAL('currentIndexChanged(int)'),
                self.update_algo)

        # heuristic chooser
        self.heuristic_combo = QtGui.QComboBox()
        self.heuristic_combo.addItems(SeashipMainWindow.heuristic_list)
        self.heuristic_combo.setItemIcon(0, QtGui.QIcon('icons/heur_manhattan.png'))
        self.heuristic_combo.setItemIcon(1, QtGui.QIcon('icons/heur_euclidean.png'))

        # algo settings
        settings_vbox = QtGui.QVBoxLayout()
        settings_vbox.setAlignment(Qt.AlignTop|Qt.AlignHCenter)
        settings_vbox.addWidget(QLabel("World"))
        settings_vbox.addWidget(self.world_combo)
        settings_vbox.addWidget(QLabel("Algorithm"))
        settings_vbox.addWidget(self.algo_combo)
        settings_vbox.addWidget(QLabel("Heuristics"))
        settings_vbox.addWidget(self.heuristic_combo)
        settings_widget = QtGui.QWidget()
        settings_widget.setLayout(settings_vbox)

        self.mainSplitter.addWidget(settings_widget)
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

        # reset button
        reset_button = QtGui.QAction(QtGui.QIcon('icons/reset.png'),
                'Random', self)
        reset_button.setShortcut('Ctrl+N')
        reset_button.setStatusTip('Randomize World')
        self.connect(reset_button, QtCore.SIGNAL('triggered()'),
                self.random_world)

        toolbar = self.addToolBar('Control')
        toolbar.addAction(reset_button)
        toolbar.addAction(start_button)
        toolbar.addAction(stop_button)

        # status bar
        self.statusBar()

    def update_algo(self):
        print "algo updated to", self.algo_combo.currentIndex()
        if self.algo_combo.currentIndex() == 0:
            self.algo_t = kapal.algo.Dijkstra
        if self.algo_combo.currentIndex() == 1:
            self.algo_t = kapal.algo.AStar

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
        if (self.algo_t is kapal.algo.Dijkstra or
                self.algo_t is kapal.algo.AStar):
            start_y = 2
            start_x = 2
            goal_y = 8
            goal_x = 8
            astar = self.algo_t(self.world, self.world.state(start_y,start_x),
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
