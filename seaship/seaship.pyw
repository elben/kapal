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

class WorldCanvas(object):
    STATE_OPEN = 0x01
    STATE_CLOSED = 0x02
    STATE_EXPANDED = 0x04
    STATE_PATH = 0x80

    COLOR_RED = (255, 0, 0, 255)
    COLOR_BLUE = (0, 80, 255, 255)
    COLOR_DARKBLUE = (0, 0, 128, 255)
    COLOR_GREEN = (0, 255, 0, 255)
    COLOR_YELLOW = (255, 255, 0, 255)
    COLOR_TRANSPARENT = (0, 0, 0, 0)

class World2dCanvas(QWidget, WorldCanvas):
    def __init__(self, parent=None, world_cost=None, world_cond=None,
            painter=None):
        QtGui.QWidget.__init__(self, parent)

        if world_cost is None:
            self.world_cost = [[1]]
        self.world_cost = world_cost

        if world_cond is None:
            self.world_cond = [[0]]
        self.world_cond = world_cond

        if painter is None:
            painter = QtGui.QPainter()
        self.painter = painter

        self.cell_size = 32

    def paintEvent(self, event):
        self.draw_world2d(self.painter)
        self.update()

    def draw_world2d(self, painter, world_cost=None, world_cond=None,
            x_start=0, y_start=0, x_goal=0, y_goal=0):
        if world_cost is None:
            world_cost = self.world_cost
        if world_cond is None:
            world_cond = self.world_cond
        for r in range(len(world_cost)):
            for c in range(len(world_cost[r])):
                if world_cost[r][c] == kapal.inf:
                    # obstacle
                    self.draw_square(painter, c, r,
                            color=WorldCanvas.COLOR_DARKBLUE)
                else:
                    # free space
                    self.draw_square(painter, c, r,
                            color=WorldCanvas.COLOR_BLUE)
                if world_cond[r][c] & WorldCanvas.STATE_EXPANDED:
                    # current cell was expanded
                    self.draw_square(painter, c, r,
                            color=WorldCanvas.COLOR_RED)
                if world_cond[r][c] & WorldCanvas.STATE_PATH:
                    # current cell is part of path
                    self.draw_square(painter, c, r,
                            color=WorldCanvas.COLOR_GREEN)

    def old_draw_world2d(self, painter, world_cost, world_cond,
            x_start=0, y_start=0, x_goal=0, y_goal=0):
        for r in range(len(world_cost)):
            for c in range(len(world_cost[r])):
                color = (0, 80, 255, 255)       # blue
                if world_cost[r][c] == -1:
                    color = (255, 0, 0, 255)    # red
                elif world_cost[r][c] == -2:
                    color = (0, 255, 0, 255)    # green
                elif world_cost[r][c] == kapal.inf:
                    color = (0, 0, 128, 255)       # blue
                self.draw_square(painter, c, r, color=color)

    def draw_square(self, painter, x=0, y=0, color=(0, 0, 0, 0),
            size=None, brush=None):
        if not painter.begin(self):
            print "draw_square: painter failed to begin()."
            return
        if size is None:
            size = self.cell_size
        if brush is None:
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            r, g, b, a = color
            brush.setColor(QtGui.QColor(r, g, b, a))
        padding = self.cell_size - size / 2
        painter.setBrush(brush)
        painter.drawRect(x*self.cell_size + padding, y*self.cell_size +
                padding, self.cell_size, self.cell_size)
        painter.end()

class SeashipMainWindow(QMainWindow):
    world_list = ["2D 4 Neighbors", "2D 8 Neighbors"]
    algo_list = ["Dijkstra", "A*"]
    heuristic_list = ["Manhattan", "Euclidean"]
    
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # set up planner
        self.algo_t = kapal.algo.Dijkstra
        self.world_t = kapal.world.World2d
        self.state_t = kapal.state.State2dAStar
        self.random_world(width=10)

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

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
        self.reset_world()

    def random_world(self, width=10):
        # set up world

        # World2d
        self.c = kapal.tools.rand_cost_map(width, width, 1, kapal.inf,
                flip=True, flip_chance=.1)
        self.world_cond = [ [0]*len(self.c[0]) for i in range(len(self.c)) ]
        self.world = kapal.world.World2d(self.c, state_type = kapal.state.State2dAStar)

    def reset_world(self):
        self.world_cond = [ [0]*len(self.c[0]) for i in range(len(self.c)) ]
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
                cond = self.world_cond[s.y][s.x]
                self.world_cond[s.y][s.x] = cond|WorldCanvas.STATE_EXPANDED
                num_popped += 1
            print num_popped
            for s in astar.path():
                cond = self.world_cond[s.y][s.x]
                self.world_cond[s.y][s.x] = cond|WorldCanvas.STATE_PATH

    def paintEvent(self, event):
        self.worldcanvas.world_cost = copy.deepcopy(self.c)
        self.worldcanvas.world_cond = self.world_cond
        self.update()

app = QtGui.QApplication(sys.argv)
seawin = SeashipMainWindow()
seawin.show()
app.exec_()
