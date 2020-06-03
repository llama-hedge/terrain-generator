import random

import numpy as np

from skimage.morphology import skeletonize
from skimage.transform import swirl
from skimage.filters import gaussian
from perlin_base import noise_arrays
from display import show_land
from utils import label_and_wrap, swiggle
import matplotlib.pyplot as plt


def add_mountains(z_array, inland=True):
    rows, columns = z_array.shape

    max_height = np.max(z_array)
    mask = np.zeros_like(z_array)
    if inland:
        mask[z_array > max_height * 0.03] = 1
    else:
        mask[z_array > -0.005 * max_height] = 1

    # label resulting landmasses
    labeled_islands = label_and_wrap(mask)
    continents = np.unique(labeled_islands, return_counts=True)
    continent_indices = [continents[0][i] for i in range(len(continents[0]))
                  if continents[0][i] != -1 and continents[1][i] > 0.0005*rows*columns]
    # choose a random selection of islands including at most 6; ignore islands less than 0.0005 of the total surface area
    n_mountains = 0

    while n_mountains < 6:
        # create at most six mountain ranges
        # if you run out of continents, break out of the loop
        for index in continent_indices:
            if random.random() > 0.8:
                # don't do all the continents
                continue
            cutter = np.zeros_like(z_array)
            cutter[labeled_islands == index] = 1
            # offset the cutter by a random amount
            x_perturb = random.randint(-int(0.05*columns), int(0.05*columns))
            y_perturb = random.randint(-int(0.05*rows), int(0.05*rows))
            offset_cutter = np.roll(cutter, (x_perturb, y_perturb), axis=(1, 0))

            sliver = cutter
            sliver[offset_cutter == 1] = 0
            # sliver is the overall shape of the mountain range.
            sliver = skeletonize(sliver)
            # Now use noise and filters to give it the right texture, then add it to the terrain
            # warp at ten random points
            sliver = swiggle(sliver)
            # blur the line
            sliver = gaussian(sliver)
            # multiply by noise to roughen
            _, _, rough_noise = noise_arrays(rows, columns, 1280)
            rough_noise += 1
            sliver *= rough_noise * 1.5
            if not inland:
                sliver *= 1.2

            z_array += sliver
            n_mountains += 1
            if n_mountains >= 6:
                break
        else:
            break
    return z_array

if __name__ == "__main__":
    # TODO convert this to a function

    # create mask slightly higher than sea level
    # zs is scaled to have sea level at 0
    zs = np.loadtxt('maps/02_drop_islands/array0.csv', delimiter=',')
    zs = add_mountains(zs, inland=True)

    mask = np.zeros_like(zs)
    mask[zs < 0] = 1
    show_land(zs, mask)