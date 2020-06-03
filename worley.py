import numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import product
from math import sqrt
from utils import swiggle


def worley(point_array):
    tone_array = np.zeros_like(point_array)
    rows, columns = point_array.shape
    points = tuple(zip(*np.where(point_array == 1)))
    for i, j in product(range(rows), range(columns)):
        lengths = [((x, y), sqrt((x-i)**2 + (y-j)**2)) for x, y in points]
        lengths.sort(key=lambda k: k[1])
        distance = lengths[0][1]
        tone_array[i, j] = tone(distance)
    return tone_array


def tone(distance):
    return distance**2


if __name__ == '__main__':
    # ROWS = 1650
    # COLUMNS = 1950
    # # generate 50 random coordinates to base noise on
    # center_points = np.zeros((ROWS, COLUMNS))
    # for i in range(200):
    #     x, y = random.randint(0, ROWS-1), random.randint(0, COLUMNS-1)
    #     center_points[x, y] = 1
    # image = worley(center_points)
    # image = swiggle(image)
    # np.savetxt(f'art/worley.csv', image, delimiter=',')
    # plt.imshow(image)
    zs = np.loadtxt('art/worley.csv', delimiter=',')
    my_dpi = 96
    fig = plt.figure(figsize=(1950 / my_dpi, 1650 / my_dpi), dpi=my_dpi)

    mpl.rcParams['savefig.pad_inches'] = 0
    ax = plt.axes([0, 0, 1, 1], frameon=False)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)

    # Plot the data.
    plt.pcolormesh(zs)
    plt.savefig('worley.png')
    plt.show()
