from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import random

generator = OpenSimplex()


def noise_arrays(a, b, freq, gen=generator):
    def noise(p, q):
        # rescale from -1, 1 to 0, 1
        return gen.noise2d(p, q)

    ys = np.linspace(start=0, stop=a - 1, num=a)
    xs = np.linspace(start=0, stop=b - 1, num=b)

    xs, ys = np.meshgrid(xs, ys)

    zs = np.zeros((a, b))

    for y in range(b):
        for x in range(a):
            nx = x / a - 0.5
            ny = y / b - 0.5
            zs[x][y] = noise(freq * nx, freq * ny)

    return xs, ys, zs


def layered_simplex(rows, columns):
    ratio_frequency_before = [
        #
        (0.5, 10),
        (0.25, 20),
        (0.12, 40),
        (0.06, 80),
        (0.03, 160),
        (0.01, 320),
    ]
    ratio_frequency_after = [
        (0.001, 1280),
    ]
    generator_a = OpenSimplex(seed=random.randint(0, 255))
    xs, ys, zs_a = noise_arrays(rows, columns, freq=5, gen=generator_a)
    for ratio, frequency in ratio_frequency_before:
        zs_a += ratio * noise_arrays(rows, columns, freq=frequency, gen=generator_a)[2]

    zs_a = np.sign(zs_a) * abs(zs_a) ** 3

    for ratio, frequency in ratio_frequency_after:
        zs_a += ratio * noise_arrays(rows, columns, freq=frequency, gen=generator_a)[2]

    generator_b = OpenSimplex(seed=random.randint(0, 255))
    _, _, zs_b = noise_arrays(rows, columns, freq=5, gen=generator_b)

    for ratio, frequency in ratio_frequency_before:
        zs_b += ratio * noise_arrays(rows, columns, freq=frequency, gen=generator_b)[2]

    zs_b = np.sign(zs_b) * abs(zs_b) ** 3

    for ratio, frequency in ratio_frequency_after:
        zs_b += ratio * noise_arrays(rows, columns, freq=frequency, gen=generator_a)[2]

    zs_a *= -(np.cos(xs * np.pi / (columns / 2)) - 1) / 2

    zs_b = np.concatenate((zs_b[:, int(columns / 2):columns], zs_b[:, 0:int(columns / 2)]), axis=1)
    zs_b *= (np.cos(xs * np.pi / (columns / 2)) + 1) / 2

    zs_t = zs_a + zs_b

    return xs, ys, zs_t


if __name__ == "__main__":
    xx, yy, zz = noise_arrays(200, 200, freq=7)

    figure = plt.figure(figsize=(10, 10))
    ax = figure.add_subplot(111, projection='3d')
    Axes3D(figure).plot_surface(xx, yy, zz, cmap='terrain')
    plt.show()
    axheat = sns.heatmap(zz, cmap='terrain')
    plt.show()
