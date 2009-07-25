from state import *
import math

class World:
    """
    World is the base class for all other world types.
    This class shows the primitive functions that all other worlds
    should implement.

    An algorithm may assume that all the functions defined here are
    implemented for any world.
    """
    def succ(self, s):
        pass
    def pred(self, s):
        pass
    def c(self, s1, s2):
        pass
    def h(self, s1, s2):
        pass
    def change_c(self, s1, s2, c):
        pass
    def reset(self):
        """An algorithm may reset the world to 'start from scratch.'"""
        pass

class World2d(World):
    def __init__(self, costs=None, state_type=State2d, diags=False, diags_mult=1.42):
        self.states = []
        self.costs = costs
        self.diags = diags
        self.diags_mult = diags_mult

        for r in range(len(costs)):
            world_l = []
            self.states.append(world_l)
            for c in range(len(costs[r])):
                world_l.append(state_type(r, c))

    def succ(self, s):
        # order: [1][2][3]        [ ][1][ ]
        #        [4][ ][5]   or   [2][ ][3]
        #        [6][7][8]        [ ][4][ ]

        succs = []
        for i in range(-1, 2):
            y = s.y + i
            for j in range(-1, 2):
                x = s.x + j 
                if not self.in_bounds(y, x):    # out of bounds
                    continue
                if y == s.y and x == s.x:   # self cannot have self as neigh
                    continue
                cost = self.costs[y][x]
                edge_count = abs(i) + abs(j)
                if edge_count == 2 and not self.diags:
                    continue    # ignore diags if requested
                elif edge_count == 2:
                    cost *= self.diags_mult     # diags allowed, so mult cost
                succs.append((self.states[y][x], cost))
        return succs

    def pred(self, s):
        return self.succ(s)

    def c(self, s1, s2):
        return costs[s2.y][s2.x]

    def h(self, s1, s2):
        dy = abs(s2.y - s1.y)
        dx = abs(s2.x - s1.x)
        return math.sqrt(dx**2 + dy**2)

    def change_c(self, s1, s2, c):
        if not self.in_bounds(s2.y, s2.x):
            return False
        self.costs[s2.y][s2.x] = c
        return True

    def reset(self):
        for r in self.states:
            for c in r:
                c.reset()

    def state(self, y, x):
        return self.states[y][x]

    def in_bounds(self, y, x):
        size_y, size_x = self.size()
        return y >= 0 and y < size_y and x >= 0 and x < size_x

    def size(self, col = 0):
        return (len(self.states), len(self.states[col]))

    def __str__(self):
        s = "World2d\n"
        s += "y size: " + str(len(self.states)) + "\n"
        s += "x size: " + str(len(self.states[0])) + "\n"
        return s
