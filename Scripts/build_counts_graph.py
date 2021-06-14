import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import json
import sys
import os

f = open(os.path.join(sys.argv[1], 'counts.json'), 'r')
counts = json.load(f)
f.close()

initial_population_size = int(sys.argv[2])
counts = [c[initial_population_size:] for c in counts]

def make_multi_line_plot(counts_list, title, save_name, max_y):
    fig, ax = plt.subplots()
    X = [x for x in range(len(counts_list[0]))]
    for counts in counts_list:
        ax.plot(X, counts)

    ax.set_ylim([0, max_y])
    ax.set_title(title)
    ax.set(xlabel='Iteration', ylabel='Usable Segments')
    fig.savefig(os.path.join(sys.argv[1], save_name))
    plt.close(fig)

max_y = max([max(c) for c in counts])


print('building n-gram graph')
make_multi_line_plot(counts, 'Gram-Elites', 'all_lines.png', max_y)

def build_data(counts):
    X = []
    Y = []

    for c in counts:
        x = 0
        for y in c:
            Y.append(y)
            X.append(x)
            x += 1

    return X, Y

print('building cumulative')
ngo_df = pd.DataFrame()
X, Y = build_data(counts)
ngo_df['X'] = X
ngo_df['Y'] = Y
sns.lineplot(data=ngo_df, x='X', y='Y')



plt.title('Usable Segments Per Iteration')
plt.xlabel('Iteration')
plt.ylabel('Usable Strands')
plt.savefig(os.path.join(sys.argv[1], 'counts.png'))
