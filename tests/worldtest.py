import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from world import *

c =  [[0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [9, 1, 2]]
w = World2d(c, state_type = State2dAStar)

######  Header  ######
print "Testing world.World2d:"

######  Test 1  ######
# successors
s = w.world[2][1]
c1 = [4, 6, 8, 1]
c2 = []
for i, j in w.succ(s):
    c2.append(j)
if c1 != c2:
    print "1: Failed."

######  Test 2  ######
# predecessors
s = w.world[0][0]
c1 = [1, 3]
c2 = []
for i, j in w.pred(s):
    c2.append(j)
if c1 != c2:
    print "2: Failed."

######  Test 3  ######
# change cost
s1 = w.world[0][0]
s2 = w.world[0][1]
w.change_c(s1, s2, 100)
c1 = [100, 3]
c2 = []
for i, j in w.pred(s):
    c2.append(j)
if c1 != c2:
    print "3: Failed."

###### Footer ######
print "Done."
