import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from display import newcmp
from inland_mountains import add_mountains
from utils import csv_to_image

steps = ['simplex', 'drop_islands', 'inland_mountains', 'coastal_mountains']

csv_to_image('art/worley.csv', 'summer_worley.png', (1950, 1650), cmap='summer')