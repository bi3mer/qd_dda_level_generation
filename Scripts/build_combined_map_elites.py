import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import numpy as np
import json
import sys
import os

GENETIC_INDEX = 0
STANDARD_N_INDEX = 1
STANDARD_INDEX = 2

combined_config_name = 'config_map_elites_combined.json'
config_names = [
    'config_map_elites_genetic.json',
    'config_map_elites_standard_n.json',
    'config_map_elites_standard.json'
]

f = open(os.path.join(sys.argv[1], combined_config_name), 'r')
combined_config = json.load(f)
f.close()

configs = []
for file_name in config_names:
    f = open(os.path.join(sys.argv[1], file_name), 'r')
    configs.append(json.load(f))
    f.close()

worst_performance = 1.0
matrices = []
for c in configs:
    resolution = c['resolution']
    matrix = [[np.nan for _ in range(resolution + 1)] for __ in range(resolution + 1)]

    f = open(c['data_file'])
    f.readline()
    content = f.readlines()
    f.close()

    for row in content:
        split_line = row.strip().split(',')
        matrix[int(split_line[1])][int(split_line[0])] = float(split_line[2])

    matrices.append(matrix)

genetic = 0
standard = 0
both = 0

resolution = combined_config['resolution']
matrix = [[np.nan for _ in range(resolution + 1)] for __ in range(resolution + 1)]
for y in range(resolution + 1):
    for x in range(resolution + 1):
        values = [False, False, False]
        for index, m in enumerate(matrices):
            if m[y][x] == 0:
                values[index] = True

        # this is a bit lazy but I know that standard operators won't generate 
        # anything usable but I have a check just in case
        values = tuple(values)
        if (True, False, False) == values:
            genetic += 1
            matrix[y][x] = 0.0
        elif (False, True, False) == values:
            standard += 1
            matrix[y][x] = 0.2
        elif (True, True, False) == values:
            both += 1
            matrix[y][x] = 0.6
        elif (False, False, False) == values:
            pass
        else:
            print(f'ERROR: handled combination: {values}')
            sys.exit(-1)

matrix = np.array(matrix)
mask = np.zeros_like(matrix)
for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        if val == np.nan:
            mask[i][j] = 1.0

color_bar_label = 'Fitness'
colors = [ 
    [0.0, "#1111FF"], # go + ngp
    [0.2, "#FF1111"], # so + ngp
    [0.4, "#00FF00"], # so + rp
    [0.6, "#AA11AA"], # so + ngp & go + ngp
    [1.0, "#FFFFFF"],
]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

x_dimensions, y_dimensions = combined_config['feature_dimensions']
resolution = int(combined_config['resolution'])
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.color_palette('viridis')
ax = sns.heatmap(
    matrix, 
    linewidths=.5, 
    square=True, 
    mask=mask,
    cmap=cmap,
    cbar=False,
    cbar_kws={'label': color_bar_label},
    vmin=0,
    vmax=worst_performance)

ax.set(xlabel=combined_config['x_label'], ylabel=combined_config['y_label'])
ax.set_xticks(ax.get_xticks()[::5])
ax.set_yticks(ax.get_yticks()[::5])

ax.legend(handles=[
    mpatches.Patch(color=colors[0][1], label='NGP + NGO'),
    mpatches.Patch(color=colors[1][1], label='NGP + SO'),
    mpatches.Patch(color=colors[3][1], label='Both')],
    fontsize='x-large')

# lower dimension is always 0 so I'm being lazy
xticks = [((x-0.5)/resolution) * x_dimensions[1] for x in ax.get_xticks().tolist()]
yticks = [((y-0.5)/resolution) * y_dimensions[1] for y in ax.get_yticks().tolist()]
ax.set_xticklabels(xticks)
ax.set_yticklabels(yticks)
plt.rcParams["axes.labelsize"] = 22

ax.set(title=combined_config['title'])
ax.invert_yaxis()
plt.savefig(combined_config['save_file'], bbox_inches="tight")
plt.close()

print(f'genetic: {genetic}')
print(f'standard: {standard}')
print(f'both: {both}')
