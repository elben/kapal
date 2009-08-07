inf = 1e100

class Planner(object):
    def __init__(self, algo, world, state):
        self.algo = algo
        self.world = world
        self.state = state
