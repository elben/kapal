from state import *

class World:
    def succ(s):
        pass
    def pred(s):
        pass
    def c(s1, s2):
        pass
    def change_c(s1, s2, c):
        pass

class World2d(World):
    def __init__(self, costs=None, state_type=State2d, diags=False, diags_mult=1.42):
        self.world = []
        self.costs = costs
        self.diags = diags
        self.diags_mult = diags_mult

        for r in range(len(costs)):
            world_l = []
            self.world.append(world_l)
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
                if not self.in_bounds(y, x):
                    # out of bounds
                    continue
                if y == s.y and x == s.x:
                    # self cannot be successor of self
                    continue
                cost = self.costs[y][x]
                edge_count = abs(i) + abs(j)
                if edge_count == 2 and not self.diags:
                    continue
                elif edge_count == 2:
                    cost *= self.diags_mult
                succs.append((self.world[y][x], cost))
        return succs

    def pred(self, s):
        return self.succ(s)

    def c(self, s1, s2):
        return costs[s2.y][s2.x]

    def change_c(self, s1, s2, c):
        if not self.in_bounds(s2.y, s2.x):
            return False
        self.costs[s2.y][s2.x] = c
        return True

    def in_bounds(self, y, x):
        size_y, size_x = self.size()
        return y >= 0 and y < size_y and x >= 0 and size_x

    def size(self, col = 0):
        return (len(self.world), len(self.world[col]))

    def __str__(self):
        s = "World2d\n"
        s += "y size: " + str(len(self.world)) + "\n"
        s += "x size: " + str(len(self.world[0])) + "\n"
        return s
