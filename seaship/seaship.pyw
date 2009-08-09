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
    STATE_START = 0x10
    STATE_GOAL = 0x20
    STATE_PATH = 0x80

    COLOR_RED = (255, 0, 0, 255)
    COLOR_REDTRAN = (255, 0, 0, 128)
    COLOR_BLUE = (0, 80, 255, 255)
    COLOR_DARKBLUE = (0, 0, 128, 255)
    COLOR_GREEN = (0, 255, 0, 255)
    COLOR_YELLOW = (255, 255, 0, 255)
    COLOR_TRANSPARENT = (0, 0, 0, 0)

    def __init__(self):
        self.painter = QtGui.QPainter()

    def draw_image(self, image, x=0, y=0):
        if not self.painter.begin(self):
            print "draw_image: self.painter failed to begin()."
            return
        point = QtCore.QPoint(x*self.cell_size, y*self.cell_size)
        self.painter.drawImage(point, image)
        self.painter.end()

    def draw_square(self, x=0, y=0, color=(0, 0, 0, 0),
            size=None, brush=None, image=None):
        if not self.painter.begin(self):
            print "draw_square: self.painter failed to begin()."
            return
        if size is None:
            size = self.cell_size
        if brush is None:
            brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
            brush.setColor(QtGui.QColor(*color))
        padding = (self.cell_size - size) / 2
        self.painter.setBrush(brush)
        
        self.painter.drawRect(x*self.cell_size + padding, y*self.cell_size +
                padding, size, size)
        self.painter.end()

    def draw_line(self, x1=0, y1=0, x2=0, y2=0, pen=None):
        if not self.painter.begin(self):
            print "draw_line: self.painter failed to begin()."
            return

        if pen is None:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine)
            pen.setColor(QtGui.QColor(*WorldCanvas.COLOR_GREEN))
        self.painter.setPen(pen)

        # padding inside cell
        padding = self.cell_size/2
        self.painter.drawLine(x1*self.cell_size+padding,
                y1*self.cell_size+padding, x2*self.cell_size+padding,
                y2*self.cell_size+padding)
        self.painter.end()

class World2dCanvas(QWidget, WorldCanvas):
    def __init__(self, parent=None, world_cost=None, world_cond=None,
            painter=None):
        QtGui.QWidget.__init__(self, parent)

        # cost of cells in the world
        if world_cost is None:
            self.world_cost = [[1]]
        self.world_cost = world_cost

        # world_cond is a 2d grid, where each cell holds
        # the condition of that cell
        if world_cond is None:
            self.world_cond = [[0]]
        self.world_cond = world_cond

        # size of each world cell drawn
        self.cell_size = 32

        if painter is None:
            painter = QtGui.QPainter()
        self.painter = painter

    def paintEvent(self, event):
        self.draw_world2d()
        self.update()

    def draw_world2d(self, x_start=0, y_start=0, x_goal=0,
            y_goal=0):

        # previous c, r values of the path, for drawing path lines
        c_prev = -1
        r_prev = -1

        for r in range(len(self.world_cost)):
            for c in range(len(self.world_cost[r])):
                if self.world_cost[r][c] == kapal.inf:
                    # obstacle
                    self.draw_square(c, r, color=WorldCanvas.COLOR_DARKBLUE)
                else:
                    # free space
                    self.draw_square(c, r, color=WorldCanvas.COLOR_BLUE)
                
                # show state of cell

                if self.world_cond[r][c] & WorldCanvas.STATE_PATH:
                    # current cell is part of path
                    if c_prev != -1:
                        self.draw_line(c, r, c_prev, r_prev)
                    c_prev = c
                    r_prev = r

                if self.world_cond[r][c] & WorldCanvas.STATE_EXPANDED:
                    # current cell was expanded
                    self.draw_square(c, r, color=WorldCanvas.COLOR_RED,
                            size=8)

                # draw ship and goal points
                if self.world_cond[r][c] & WorldCanvas.STATE_START:
                    ship_img = QtGui.QImage("icons/ship.png")
                    self.draw_image(ship_img, c, r)

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
            self.world_cond[start_y][start_x] |= WorldCanvas.STATE_START
            astar = self.algo_t(self.world, self.world.state(start_y,start_x),
                    self.world.state(goal_y, goal_x))
            #astar.h = fake_h
            num_popped = 0
            for s in astar.plan_gen():
                self.world_cond[s.y][s.x] |= WorldCanvas.STATE_EXPANDED
                num_popped += 1
            print num_popped
            for s in astar.path():
                self.world_cond[s.y][s.x] |= WorldCanvas.STATE_PATH

    def paintEvent(self, event):
        self.worldcanvas.world_cost = copy.deepcopy(self.c)
        self.worldcanvas.world_cond = self.world_cond
        self.update()

app = QtGui.QApplication(sys.argv)
seawin = SeashipMainWindow()
seawin.show()
app.exec_()
