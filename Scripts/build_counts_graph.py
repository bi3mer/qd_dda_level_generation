import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import json
import sys
import os

f = open(os.path.join(sys.argv[1], 'counts.json'), 'r')
counts = json.load(f)
f.close()

def make_multi_line_plot(counts_list, title, save_name, max_y):
    fig, ax = plt.subplots()
    X = [x for x in range(len(counts_list[0]))]
    for counts in counts_list:
        ax.plot(X, counts)

    ax.set_ylim([0, max_y])
    ax.set_title(title)
    ax.set(xlabel='Generation', ylabel='Valid Strands')
    fig.savefig(os.path.join(sys.argv[1], save_name))
    plt.close(fig)

max_y = max(
    max([max(c) for c in counts['standard_n']]),
    max([max(c) for c in counts['ngo']]),
    max([max(c) for c in counts['grammar']]))

make_multi_line_plot(counts['standard_n'], 'Standard Operators + N-Gram Population', 'son.png', max_y)
make_multi_line_plot(counts['ngo'], 'N-Gram Genetic Operators', 'ngo.png', max_y)
make_multi_line_plot(counts['grammar'], 'N-Gram', 'ngram.png', max_y)

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

ngo_df = pd.DataFrame()
X, Y = build_data(counts['ngo'])
ngo_df['X'] = X
ngo_df['Y'] = Y
sns.lineplot(data=ngo_df, x='X', y='Y', label='NGO')

son_df = pd.DataFrame()
X, Y = build_data(counts['standard_n'])
son_df['X'] = X
son_df['Y'] = Y
sns.lineplot(data=son_df, x='X', y='Y', label='Standard Operators + N-Gram')

gram_df = pd.DataFrame()
X, Y = build_data(counts['grammar'])
gram_df['X'] = X
gram_df['Y'] = Y
sns.lineplot(data=gram_df, x='X', y='Y', label='N-Gram')

plt.title('Valid Segments Per Generation')
plt.xlabel('Generation')
plt.ylabel('Valid Strands')
plt.legend()
plt.savefig(os.path.join(sys.argv[1], 'counts.png'))
