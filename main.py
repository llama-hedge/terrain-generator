from perlin_base import layered_simplex
from sink import sink
from inland_mountains import add_mountains

import numpy as np

if __name__ == "__main__":
    COLUMNS = 400
    ROWS = 200

    # step one
    # for i in range(10):
    #     xs, ys, zs = layered_simplex(ROWS, COLUMNS)
    #     np.savetxt(f'maps/01_simplex/array{i}.csv', zs, delimiter=',')

    # step two - sink extra islands
    for i in range(10):
        zs = np.loadtxt(f'maps/01_simplex/array{i}.csv', delimiter=',')
        zs, labels = sink(zs)
        np.savetxt(f'maps/02_drop_islands/array{i}.csv', zs, delimiter=',')
        np.savetxt(f'maps/02_drop_islands/array{i}_labels.csv', zs, delimiter=',')

    # step three - inland mountains
    for i in range(10):
        zs = np.loadtxt(f'maps/02_drop_islands/array{i}.csv', delimiter=',')
        zs = add_mountains(zs)
        np.savetxt(f'maps/03_inland_mountains/array{i}.csv', zs, delimiter=',')

    # step four - coastal mountains
    for i in range(10):
        zs = np.loadtxt(f'maps/03_inland_mountains/array{i}.csv', delimiter=',')
        zs = add_mountains(zs, inland=False)
        np.savetxt(f'maps/04_coastal_mountains/array{i}.csv', zs, delimiter=',')
