# collection of random tools
import random
import kapal

def rand_cost_map(y_size=1, x_size=1, min_val=1, max_val=kapal.inf,
        flip=False, flip_chance=.1):
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
