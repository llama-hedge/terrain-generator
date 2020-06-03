import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


zs = np.loadtxt(f'maps/04_coastal_mountains/array0.csv', delimiter=',')
rows, columns = zs.shape

ys = np.linspace(start=0, stop=rows - 1, num=rows)
xs = np.linspace(start=0, stop=columns - 1, num=columns)
xs, ys = np.meshgrid(xs, ys)

zs[zs < 0] = 0
figure = plt.figure(figsize=(10, 20))
ax = figure.add_subplot(111, projection='3d')
Axes3D(figure).plot_surface(xs, ys, zs, cmap='terrain')
plt.show()