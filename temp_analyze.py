from json import load
from Config import Mario, Icarus, DungeonGram
from os.path import join

from Utility.Math import median, mean, rmse
from statistics import stdev
import matplotlib.pyplot as plt 
from itertools import chain


NO_LINK = 'no_link'
FIRST = 'first'
BEST = 'best'
L = 'links'
BC = 'behavioral_characteristics'
C  = 'completability'
CS = 'connection_success'
CE = 'connection_error'
S = 'segments'
R = 'runs'
G = 'is_generable'

headers = ['', 'min', 'mean', 'median', 'max', 'std']
format_row = "{:>9}" * (len(headers))

def build_row(name, scores):
    return [
        name,
        round(min(scores), 3),
        round(mean(scores), 3),
        round(median(scores), 3),
        round(max(scores), 3),
        round(stdev(scores), 3)
    ]

def get_and_print_stats(config):
    global headers
    global format_row

    print(config.name)
    f = open(join(config.data_dir, 'random_walkthrough_results.json'))
    stats = load(f)
    f.close()

    runs = stats['target_size']

    # behavioral characteristics
    bc = {}
    for bc_name in config.feature_names:
        bc[bc_name] = {}
        bc[bc_name][FIRST] = []
        bc[bc_name][BEST] = []

    # Link Lengths
    first_len = []
    best_len = []

    for k in stats:
        if k == 'target_size':
            continue
        print(f'K={k}')
        print()
        print('100% beatable levels / runs')
        print(f'{NO_LINK}: {sum([NO_LINK in r for r in stats[k][R]])} / {runs}')
        print(f'{FIRST}: {sum([FIRST in r for r in stats[k][R]])} / {runs}')
        print(f'{BEST}: {sum([BEST in r for r in stats[k][R]])} / {runs}')

        print()
        print('100% beatable levels / levels with links')
        print(f'{NO_LINK}: {sum([r[NO_LINK][C] == 1.0 for r in stats[k][R] if NO_LINK in r])} / {sum([NO_LINK in r for r in stats[k][R]])}')
        print(f'{FIRST}: {sum([r[FIRST][C] == 1.0 for r in stats[k][R] if FIRST in r])} / {sum([FIRST in r for r in stats[k][R]])}')
        print(f'{BEST}: {sum([r[BEST][C] == 1.0 for r in stats[k][R] if BEST in r])} / {sum([BEST in r for r in stats[k][R]])}')

        # completability
        print()
        print()
        print('Completability')
        first = []
        best = []
        no_link = []
        for r in stats[k][R]:
            if NO_LINK in r:
                no_link.append(r[NO_LINK][C])
        
            if FIRST in r:
                first.append(r[FIRST][C])
                best.append(r[BEST][C])

        table = [
            build_row(NO_LINK, no_link),
            build_row(FIRST, first),
            build_row(BEST, best),
        ]
        
        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))
        print()
        print()

        # generability
        no_link = []
        first = []
        best = []

        for r in stats[k][R]:
            if NO_LINK in r:
                no_link.append(r[NO_LINK][G])

            if FIRST in r:
                first.append(r[FIRST][G])
                best.append(r[BEST][G])

        table = [
            build_row(NO_LINK, no_link),
            build_row(FIRST, first),
            build_row(BEST, best),
        ]

        print('Generability')
        format_row = "{:>9}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))

        print()
        print('Usable')
        print(f'{NO_LINK}: {sum([r[NO_LINK][C] == 1.0 for r in stats[k][R] if NO_LINK in r and r[NO_LINK][G]])} / {sum([NO_LINK in r for r in stats[k][R]])}')
        print()
        print()

        # BC
        for r in stats[k][R]:
            for i in range(len(config.feature_names)):
                if FIRST in r:
                    bc[config.feature_names[i]][FIRST].append(r[FIRST][BC][i])
                    bc[config.feature_names[i]][BEST].append(r[BEST][BC][i])

        # link lengths
        for r in stats[k][R]:
            if FIRST in r:
                first_len.extend([len(l) for l in r[FIRST][L]])
                best_len.extend([len(l) for l in r[BEST][L]])

    
        print('===============================================================')
        print()

    print()
    print('===============================================================')
    print('===============================================================')

    return first_len, best_len, bc


def link_lengths(config, first_len, best_len, bc):
    for index, bc_name in enumerate(config.feature_names):
        table = []
        print(bc_name)
        table.append(build_row(FIRST, bc[bc_name][FIRST]))
        table.append(build_row(BEST, bc[bc_name][BEST]))

        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))
        print()
        print()

    print()
    print('link Length')
    table = []
    table.append(build_row(FIRST, first_len))
    table.append(build_row(BEST, best_len))

    print(format_row.format(*headers))
    for _, row in zip(headers, table):
        print(format_row.format(*row))

def plot_link_lengths(stuff):
    # feeling laxy, stuff is an array of tuples with (config, first_len, best_len).
    fig, ax = plt.subplots()
    ax.boxplot(
        list(chain(*[(s[1], s[2]) for s in stuff])), 
        labels=list(chain(*[(f'{s[0].name}\n{FIRST}', f'{s[0].name}\n{BEST}') for s in stuff])), 
        vert=False)

    ax.yaxis.set_tick_params(labelsize='xx-small')
    ax.set_title(f'Link Lengths')
    ax.set_xlabel('Link Length')
    plt.savefig(join('link_link_lengths.pdf'))
    plt.close(fig)

def plot_bc(config, bc):
    fig, ax = plt.subplots()
    ax.boxplot(
        [bc[f_name][alg] for f_name in bc for alg in [FIRST, BEST]],
        labels=[f'{f_name}\n{alg}' for f_name in bc for alg in [FIRST, BEST]],
        vert=False)
    ax.set_title(f'{config.name} Behavioral Characteristic RMSE')
    ax.set_xlabel('RMSE')
    plt.savefig(join(config.data_dir, 'link_bc.pdf'))
    plt.close(fig)

m_first_len, m_best_len, m_bc = get_and_print_stats(Mario)
i_first_len, i_best_len, i_bc = get_and_print_stats(Icarus)
d_first_len, d_best_len, d_bc = get_and_print_stats(DungeonGram)

plot_link_lengths([
    (Mario, m_first_len, m_best_len),
    (Icarus, i_first_len, i_best_len,),
    (DungeonGram, d_first_len, d_best_len,),
])

plot_bc(Mario, m_bc)
plot_bc(Icarus, m_bc)
plot_bc(DungeonGram, m_bc)

