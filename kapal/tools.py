import random
import kapal

def rand_cost_map(y_size=1, x_size=1, min_val=1, max_val=kapal.inf,
        flip=False, flip_chance=.1):
    """
    Returns a 2d cost matrix with random values.

    Args:
        y_size - width
        x_size - height
        min_val - minimum random value
        max_val - maximum random value
        flip - if True, then the value in each cell is either min_val
               or max_val;
               if False, then min_val <= value of cell <= max_val
        flip_chance - chance of getting a max_val (only if flip=True)
    """
    map = []
    for i in range(y_size):
        row = []
        for j in range(x_size):
            if flip:
                if random.random() < flip_chance:
                    row.append(max_val) 
                else:
                    row.append(min_val)
            else:
                row.append(random.randint(min_val, max_val))
        map.append(row)
    return map
