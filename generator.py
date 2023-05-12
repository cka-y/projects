import random

import numpy as np


def generate_precincts(precincts_x, precincts_y, filename):
    assert precincts_x >= 0 and precincts_y >= 0
    precincts_map = [[random.randint(0, 100) for _ in range(precincts_x)] for _ in range(precincts_y)]
    with open('./exemplaires/' + f'{filename}.txt', 'w') as f:
        f.write(str(precincts_x) + " " + str(precincts_y) + "\n")
        np.savetxt(f, np.array(precincts_map), fmt="%-3.0i")

