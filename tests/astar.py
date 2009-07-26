import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from algo import *
from world import *
from state import *
import tools
import time

def main():
    """
    c =  [[0, 1, 2],
          [3, 4, 5],
          [6, 7, 8],
          [9, 1, 2]]
    """
    width = 50
    max_width = 300
    x_axis = []
    time = []
    while width < max_width:
        print width

        c = tools.rand_cost_map(250, 250, 1, 3, flip=True)
        w = World2d(c, state_type = State2dAStar)

        astar = AStar(w, w.state(0,0), w.state(99, 99))
        start_time = time.time()
        astar.plan()
        time.append(time.time() - start_time)

        path = astar.path()
        x_axis.append(width)

        width += 50
    print x_axis
    print time
main()
