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
    astar = AStar(w, w.state(0,0), w.state(1, 1))
    astar.plan()
    for s in astar.plan(generate=True):
        print s

main()
