import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from algo import *
from world import *
from state import *

def main():
    c =  [[0, 1, 2],
          [3, 4, 5],
          [6, 7, 8],
          [9, 1, 2]]
    w = World2d(c, state_type = State2dAStar)
    astar = AStar(w, w.state(0,0), w.state(3, 2))
    astar.plan()
    path = astar.path()
    for s in path:
        print s

main()
