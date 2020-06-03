import numpy as np
import matplotlib.pyplot as plt

import random

from utils import label_and_wrap


def sink(z_array):
    water = np.percentile(z_array, 70)

    land_array = np.zeros_like(z_array)
    land_array[z_array > water] = 1.0

    labeled_islands = label_and_wrap(land_array)

    # assign labels_and_sizes after wrap
    labels_and_sizes = [(i, np.sum(labeled_islands == i)) for i in np.unique(labeled_islands)]
    labels_and_sizes.sort(key=lambda x: x[1])

    # keep the largest island, then randomly sink about a third of the rest
    sinkable = labels_and_sizes[:-2]
    for index_label, size in sinkable:
        k = random.random()
        if k < 1/3:
            z_array[labeled_islands == index_label] *= -1
            labeled_islands[labeled_islands == index_label] = -1
    # TODO check whether a valid dateline exists and sink an island if necessary
    

    z_array -= water
    return z_array, labeled_islands


if __name__ == "__main__":
    zs = np.loadtxt('maps/01_simplex/array3.csv', delimiter=',')
    waterline = np.percentile(zs, 70)
    land = np.zeros_like(zs)
    land[zs < waterline] = 1

    zs, label_array = sink(zs)
    # show_land(zs, land)
    plt.imshow(label_array)
    plt.show()
