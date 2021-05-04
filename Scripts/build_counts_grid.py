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

colors = [
    [0.0, "#aa444455"],
    [0.00000001, "#DDD"],
    [1.0, "#00AA00FF"],
]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)


for method in data['methods']:
    matrix = [[0 for _ in range(resolution + 1)] for __ in range(resolution + 1)]
    grid = data['methods'][method]
    for key in grid:
        x, y = eval(key)
        if y > resolution:
            print(f'Warning: received too large of y: {y} > {resolution}')
            continue
        if x > resolution:
            print(f'Warning: received too large of x: {x} > {resolution}')
            continue

        matrix[y][x] = (grid[key] / runs)*100

    # mask = np.zeros_like(matrix)
    # for i, row in enumerate(matrix):
    #     for j, val in enumerate(row):
    #         if val == np.nan:
    #             mask[i][j] = 1.0

    sns.set(rc={'figure.figsize':(11.7,8.27)})
    ax = sns.heatmap(
        matrix, 
        linewidths=.5, 
        square=True,
        cmap=cmap,
        # mask=mask,
        cbar_kws={'label': '% Runs Found Bin'},
        vmin=0,
        vmax=100
    )

    ax.set(xlabel=data['x_label'], ylabel=data['y_label'])
    ax.set_xticks(ax.get_xticks()[::5])
    ax.set_yticks(ax.get_yticks()[::5])

    ax.set(title=method)
    ax.invert_yaxis()
    plt.savefig(os.path.join(sys.argv[1], f'bins_{method}.pdf'), bbox_inches="tight")
    plt.close()