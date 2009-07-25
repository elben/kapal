class State:
    pass

class State2d(State):
    def __init__(self, y=0, x=0):
        self.y = y
        self.x = x
    def __str__(self):
        return "(" + str(self.y) + ", " + str(self.x) + ")"

class State2dAStar(State2d):
    def __init__(self, y=0, x=0, g=0, h=0, bp=None):
        State2d.__init__(self, y, x)
        self.g = g
        self.h = h
        self.bp = bp
    def __str__(self):
        return (State2d.__str__(self) + ": g = " + str(self.g) + "; h = " +
            str(self.h))
