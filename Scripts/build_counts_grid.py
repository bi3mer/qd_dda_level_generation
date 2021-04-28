from itertools import zip_longest
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import numpy as np
import json
import sys
import os


f = open(os.path.join(sys.argv[1], 'bins.json'))
data = json.load(f)
f.close()

runs = data['runs']
resolution = data['resolution']

for method in data['methods']:
    matrix = [[0 for _ in range(resolution + 1)] for __ in range(resolution + 1)]
    grid = data['methods'][method]
    for key in grid:
        x, y = eval(key)
        matrix[y][x] = grid[key] / runs

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax = sns.heatmap(
        matrix, 
        linewidths=.5, 
        square=True,
        cmap='Greens',
        cbar_kws={'label': '% Runs Found Bin'},
        vmin=0,
        vmax=1
    )

    ax.set(xlabel=data['x_label'], ylabel=data['y_label'])
    ax.set_xticks(ax.get_xticks()[::5])
    ax.set_yticks(ax.get_yticks()[::5])

    ax.set(title=method)
    ax.invert_yaxis()
    plt.savefig(os.path.join(sys.argv[1], f'bins_{method}.pdf'), bbox_inches="tight")
    plt.close()