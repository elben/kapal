class State:
    pass

class State2d(State):
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x
    def __str__(self):
        return "(" + str(self.y) + ", " + str(self.x) + ")"

class State2dAStar(State2d):
    #inf = float('inf')
    inf = 1e100
    def __init__(self, y=0, x=0, g=inf, h=0, bp=None):
        State2d.__init__(self, y, x)
        self.g = g
        self.h = h
        self.bp = bp
    def __cmp__(self, other):
        # TODO: allow any key function?
        # heapq library is a min heap
        self_f = self.g + self.h
        other_f = other.g + other.h
        if self_f < other_f or (self_f == other_f and self.g > other.g):
            # priority(self) > priority(other), so self < other
            return -1
        elif self_f == other_f and self.g == other.g:
            return 0
        return 1

    def __str__(self):
        s = State2d.__str__(self) + "-->"
        if self.bp is None:
            s += "None"
        else:
            s += State2d.__str__(self.bp)
        s += ": g = " + str(self.g) + "; h = " + str(self.h)
        return s
