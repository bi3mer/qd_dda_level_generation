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

color_bar_label = 'Percent Playable'
resolution = 50

norm = matplotlib.colors.Normalize(0,1)
colors = [
    [0.0, "#ff000011"],
    [0.99, "#ff0000ff"],
    [1.0, "green"]
]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

f = open(config['data_file'])
f.readline()
content = f.readlines()
f.close()

matrix = [[np.nan for _ in range(resolution)] for __ in range(resolution)]
for row in content:
    split_line = row.strip().split(',')
    matrix[int(split_line[1])][int(split_line[0])] = float(split_line[2])
matrix = np.array(matrix)

mask = np.zeros_like(matrix)
for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        if val == np.nan:
            mask[i][j] = 1.0

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
    vmax=1)

ax.set(xlabel=config['x_label'], ylabel=config['y_label'])
ax.set(xticklabels=[], yticklabels=[])
ax.set(title=config['title'])
ax.invert_yaxis()
plt.show()
# plt.savefig(config['save_file'], bbox_inches="tight") 
# os.remove(sys.argv[1])
print('Saved MAP-Elites graph and deleted configuration file.')
