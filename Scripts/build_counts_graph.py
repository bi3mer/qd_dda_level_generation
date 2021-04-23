import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import json
import sys
import os

f = open(os.path.join(sys.argv[1], 'counts.json'), 'r')
counts = json.load(f)
f.close()

initial_population_size = 500
counts['standard_n'] = [c[initial_population_size:] for c in counts['standard_n']]
counts['ngo'] = [c[initial_population_size:] for c in counts['ngo']]
counts['grammar'] = [c[initial_population_size:] for c in counts['grammar']]

def make_multi_line_plot(counts_list, title, save_name, max_y):
    fig, ax = plt.subplots()
    X = [x for x in range(len(counts_list[0]))]
    for counts in counts_list:
        ax.plot(X, counts)

    ax.set_ylim([0, max_y])
    ax.set_title(title)
    ax.set(xlabel='Generation', ylabel='Usable Segments')
    fig.savefig(os.path.join(sys.argv[1], save_name))
    plt.close(fig)

max_y = max(
    max([max(c) for c in counts['standard_n']]),
    max([max(c) for c in counts['ngo']]),
    max([max(c) for c in counts['grammar']]))

print('building standard_n graph')
make_multi_line_plot(counts['standard_n'], 'ME-SO', 'son.png', max_y)

print('building ngo graph')
make_multi_line_plot(counts['ngo'], 'ME-NGO', 'ngo.png', max_y)

print('building n-gram graph')
make_multi_line_plot(counts['grammar'], 'NG', 'ngram.png', max_y)

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

print('building cumulative ngo')
ngo_df = pd.DataFrame()
X, Y = build_data(counts['ngo'])
ngo_df['X'] = X
ngo_df['Y'] = Y
sns.lineplot(data=ngo_df, x='X', y='Y', label='ME-NGO')

print('building cumulative standard_n')
son_df = pd.DataFrame()
X, Y = build_data(counts['standard_n'])
son_df['X'] = X
son_df['Y'] = Y
sns.lineplot(data=son_df, x='X', y='Y', label='ME-SO')

print('building cumulative n-gram')
gram_df = pd.DataFrame()
X, Y = build_data(counts['grammar'])
gram_df['X'] = X
gram_df['Y'] = Y
sns.lineplot(data=gram_df, x='X', y='Y', label='NG')

plt.title('Usable Segments Per Generation')
plt.xlabel('Generation')
plt.ylabel('Usable Strands')
plt.legend()
plt.savefig(os.path.join(sys.argv[1], 'counts.png'))
