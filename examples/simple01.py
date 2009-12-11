from kapal.algo import *
from kapal.world import *
from kapal.state import *
import kapal.tools
import time

# TODO: walk through example with comments
# TODO: post this example on wiki as a tutorial

n = 50      # width/height of world
c = kapal.tools.rand_cost_map(n, n, min_val=1, max_val=3, flip=True)
w = World2d(c, state_type = State2dAStar)

astar = AStar(w, w.state(0,0), w.state(n-1, n-1))
start_time = time.time()
path = astar.plan()
total_time = time.time() - start_time

print total_time, "seconds."

# TODO: finish the example. show the output in a human-readable format.
#       perhaps possible interface with Seaship.
