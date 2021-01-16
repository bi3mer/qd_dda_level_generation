from os.path import split
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import numpy as np
import json
import sys
import os

print('Generating MAP-Elites graph...', sys.argv[1])

f = open(sys.argv[1], 'r')
config = json.load(f)
f.close()

color_bar_label = '# Bad Transitions + 1 - Percent Playable'
resolution = config['resolution']

f = open(config['data_file'])
f.readline()
content = f.readlines()
f.close()

worst_performance = 1.0

matrix = [[np.nan for _ in range(resolution + 1)] for __ in range(resolution + 1)]
for row in content:
    split_line = row.strip().split(',')
    worst_performance = max(worst_performance, float(split_line[2]))
    matrix[int(split_line[1])][int(split_line[0])] = float(split_line[2])
matrix = np.array(matrix)

mask = np.zeros_like(matrix)
for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        if val == np.nan:
            mask[i][j] = 1.0

colors = [
    [0.0, "green"],
    [0.00000001, "#ff000011"],
    [1.0, "#ff0000ff"],
]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.color_palette('viridis')
ax = sns.heatmap(
    matrix, 
    linewidths=.5, 
    square=True, 
    mask=mask,
    cmap=cmap,
    cbar_kws={'label': color_bar_label},
    vmin=0,
    vmax=worst_performance)

ax.set(xlabel=config['x_label'], ylabel=config['y_label'])
ax.set(xticklabels=[], yticklabels=[])
ax.set(title=config['title'])
ax.invert_yaxis()
plt.savefig(config['save_file'], bbox_inches="tight") 
