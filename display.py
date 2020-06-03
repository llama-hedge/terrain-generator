import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import ListedColormap


gist_earth_full = cm.get_cmap('gist_earth', 512)
newcmp = ListedColormap(gist_earth_full(np.linspace(0.4, 1, 256)))


def show_land(z_array, land_mask):
    sns.heatmap(z_array, cmap=newcmp, mask=land_mask)
    plt.show()


steps = ['simplex', 'drop_islands', 'inland_mountains', 'coastal_mountains']

if __name__ == "__main__":
    f, axes = plt.subplots(len(steps), 1)
    zs = [np.loadtxt(f'maps/0{i+1}_{step}/array5.csv', delimiter=',') for i, step in enumerate(steps)]
    land = zs[0] < np.percentile(zs[0], 70)
    #
    for i, ax in enumerate(axes):
        zs[i][land == 1] = -1
        zs[i][zs[i] < 0] = -1
        land = zs[i] < 0
        ax.imshow(zs[i], cmap='gist_earth')
        # sns.heatmap(zs[i], cmap=newcmp, mask=land, ax=ax)
    plt.show()
