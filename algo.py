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
    def __init__(self, world, start, goal):
        Algo.__init__(self, world, start, goal)
        self.open = []
    def plan(self):
        self.start.g = 0
        self.open = [self.start]
        s = None
        while s is not self.goal:
            s = heapq.heappop(self.open)
            s.v = s.g
            print "popped:", str(s)
            for n, c in self.world.succ(s):
                if n.g > s.g + c:
                    n.g = s.g + c
                    n.h = self.world.h(n, self.goal)
                    n.bp = s
                    heapq.heappush(self.open, n)
                    print "pushed:", str(n)

