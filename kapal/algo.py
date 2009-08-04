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
        """
        Plans and returns the optimal path, from start to goal.
        """
        return list(self.plan_gen())

    def plan_gen(self):
        """
        Plans the optimal path via a generator.

        A generator that yields states as it is popped off
        the open list, which is the optimal path in A* assuming
        all assumptions regarding heuristics are held.
        """
        self.world.reset()      # forget previous search's g-vals
        goal = self.goal
        succ = self.world.succ  # successor function

        if self.backwards:
            self.goal.g = 0
            self.open = [self.goal]
            goal = self.start
            succ = self.world.pred  # flip map edges
        else:
            self.start.g = 0
            self.open = [self.start]

        # A*
        s = None
        while s is not goal and len(self.open) > 0:
            s = heapq.heappop(self.open)
            for n, cost in succ(s):
                if n.g > s.g + cost:
                    # s improves n
                    n.g = s.g + cost
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
        
    def h(self, s1, s2, h_func=None):
        """
        Returns the heuristic value between s1 and s2.

        Uses h_func, a user-defined heuristic function, if
        h_func is passed in.
        """
        if h_func is None:
            return self.world.h(s1, s2)
        else:
            return h_func(s1, s2)

