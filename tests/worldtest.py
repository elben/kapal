import sys
import os
import unittest
from kapal.world import *

class TestWorld2d(unittest.TestCase):
    def setUp(self):
        self.c =  [[0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8],
                   [9, 1, 2]]
        self.w = World2d(self.c, state_type=State2dAStar)

    ######  Test 1  ######
    # successors
    def testSucc1(self):
        s = self.w.state(2, 1)
        c1 = [4, 6, 8, 1]
        c2 = []
        for i, j in self.w.succ(s):
            c2.append(j)
        self.assertEqual(c1, c2)

    ######  Test 2  ######
    # predecessors
    def testPred1(self):
        s = self.w.state(0, 0)
        c1 = [1, 3]
        c2 = []
        for i, j in self.w.pred(s):
            c2.append(j)
        self.assertEqual(c1, c2)

    ######  Test 3  ######
    # change cost
    def testChangeCost1(self):
        s1 = self.w.state(0, 0)
        s2 = self.w.state(0, 1)
        self.w.change_c(s1, s2, 100)
        c1 = [100, 3]
        c2 = []
        for i, j in self.w.pred(s1):
            c2.append(j)
        self.assertEqual(c1, c2)

if __name__ == '__main__':
    unittest.main()

