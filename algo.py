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

    def plan(self):
        list(self.generate_plan())

    def generate_plan(self):
        self.world.reset()      # forget previous search's g-vals
        goal = self.goal
        if self.backwards:
            self.goal.g = 0
            self.open = [self.goal]
            goal = self.start
        else:
            self.start.g = 0
            self.open = [self.start]

        s = None

        # A*
        while s is not goal and len(self.open) > 0:
            s = heapq.heappop(self.open)
            for n, c in self.world.succ(s):
                if n.g > s.g + c:
                    # s improves n
                    n.g = s.g + c
                    n.h = self.h(n, self.goal)
                    n.bp = s
                    heapq.heappush(self.open, n)
            yield s

    def path(self):
        # find path from goal to the first state with bp = None
        p = []
        s = self.goal
        if self.backwards:
            s = self.start
        while s is not None:
            p.append(s)
            if s is not None:
                s = s.bp
        return p
        
    def h(self, s1, s2):
        return self.world.h(s1, s2)
