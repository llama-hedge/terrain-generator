from skimage.measure import label
from scipy.stats import mode
from skimage.transform import swirl
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def label_and_wrap(land_array):
    rows, columns = land_array.shape
    # skimage assigns a number to each island
    labeled_islands = label(land_array)
    # label ocean as -1
    ocean_label = mode(labeled_islands, axis=None)[0][0]
    labeled_islands[labeled_islands == ocean_label] = -1

    # horizontal wrap
    # force blocs on left side to match right side
    for i in range(rows):
        k = labeled_islands[i, columns - 1]
        if k == ocean_label:
            continue
        # check if there is an island directly on the other side
        opposite = labeled_islands[i, 0]
        if opposite != -1:
            labeled_islands[labeled_islands == opposite] = k
    return labeled_islands


def swiggle(image, whirls=10, strength=1.1):
    rows, columns = image.shape
    for i in range(whirls):
        center_x = random.randint(0, rows - 1)
        center_y = random.randint(0, columns - 1)
        image = swirl(image, strength=random.random() * strength, radius=(rows + columns) / 4, center=(center_y, center_x))
    return image


def csv_to_image(load_path, save_path, size, dpi=96, cmap='', show_result=True):
    zs = np.loadtxt(load_path, delimiter=',')
    plt.figure(figsize=(size[0] / dpi, size[1] / dpi), dpi=dpi)

    mpl.rcParams['savefig.pad_inches'] = 0
    ax = plt.axes([0, 0, 1, 1], frameon=False)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.autoscale(tight=True)

    plt.pcolormesh(zs, cmap=cmap)
    plt.savefig(save_path)
    if show_result:
        plt.show()
