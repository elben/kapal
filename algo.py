import heapq
from state import *
from world import *

class Algo:
    def __init__(self, world, start, goal):
        self.world = world
        self.start = start
        self.goal = goal
    def plan(self):
        pass

class AStar(Algo):
    """
    A* algorithm.
    """

    def __init__(self, world, start=None, goal=None, backwards=True):
        Algo.__init__(self, world, start, goal)
        self.backwards = backwards
        self.open = []
    def plan(self, generate=False):
        # cannot replan properly after edge cost changes... must reset all g
        # vals to inf first!
        goal = self.goal
        if self.backwards:
            self.goal.g = 0
            self.open = [self.goal]
            goal = self.start
        else:
            self.start.g = 0
            self.open = [self.start]

        s = None
        while s is not goal and len(self.open) > 0:
            s = heapq.heappop(self.open)
            # print "pop :", str(s)
            for n, c in self.world.succ(s):
                if n.g > s.g + c:
                    n.g = s.g + c
                    n.h = self.world.h(n, self.goal)
                    n.bp = s
                    heapq.heappush(self.open, n)
                    # print "push:", str(n)
            if generate:
                yield s

    def path(self):
        p = []
        s = self.goal
        start = self.start
        if self.backwards:
            s = self.start
            start = self.goal
        while s is not start:
            p.append(s)
            s = s.bp
        return p
        
    def h(self, s1, s2):
        return self.world.h(s1, s2)
