import sys
import os
from kapal.algo import *
from kapal.world import *
from kapal.state import *
import kapal.tools
import time
import matplotlib.pyplot as plt

def main():
    """
    c =  [[0, 1, 2],
          [3, 4, 5],
          [6, 7, 8],
          [9, 1, 2]]
    """
    num_runs = 1

    width = 50
    max_width = 500
    x_axis = []
    y_axis = []
    while width < max_width:
        print width

        c = tools.rand_cost_map(width, width, 1, 3, flip=True)
        w = World2d(c, state_type = State2dAStar)

        astar = AStar(w, w.state(0,0), w.state(width-1, width-1))
        start_time = time.time()
        for i in range(num_runs):
            astar.plan()
        y_axis.append((time.time() - start_time)/num_runs)

        path = astar.path()
        x_axis.append(width)

        width += 50
    print x_axis
    print y_axis
    plt.plot(x_axis, y_axis)
    plt.ylabel('time (s)')
    plt.xlabel('world size (width and height)')
    plt.show()
main()
