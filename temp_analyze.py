from json import load
from Config import Icarus as config
from os.path import join

from Utility.Math import median, mean, rmse
from statistics import stdev


def build_row(name, scores):
    return [
        name,
        round(min(scores), 3),
        round(mean(scores), 3),
        round(median(scores), 3),
        round(max(scores), 3),
        round(stdev(scores), 3)
    ]

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


f = open(join(config.data_dir, 'random_walkthrough_results.json'))
stats = load(f)
f.close()

runs = stats['target_size']

k = '3'

for k in stats:
    if k == 'target_size':
        continue
    print(f'K={k}')
    print()
    print('100% beatable levels / runs')
    print(f'{BEST}: {sum(stats[k][BEST])} / {runs}')
    print(f'{FIRST}: {sum(stats[k][FIRST])} / {runs}')
    print(f'{NO_LINK}: {sum(stats[k][NO_LINK])} / {runs}')

    print()
    print('100% beatable levels / levels with links')
    print(f'{BEST}: {sum(stats[k][BEST])} / {len(stats[k][R])}')
    print(f'{FIRST}: {sum(stats[k][FIRST])} / {len(stats[k][R])}')
    print(f'{NO_LINK}: {sum(stats[k][NO_LINK])} / {len(stats[k][R])}')

    # completability
    print()
    print()
    print('Completability')
    headers = ['', 'min', 'mean', 'median', 'max', 'std']
    first = []
    best = []
    no_link = []
    for r in stats[k][R]:
        no_link.append(r[NO_LINK][C])
        first.append(r[FIRST][C])
        best.append(r[BEST][C])

    table = [
        build_row(NO_LINK, no_link),
        build_row(FIRST, first),
        build_row(BEST, best),
    ]

    format_row = "{:>9}" * (len(headers))
    print(format_row.format(*headers))
    for _, row in zip(headers, table):
        print(format_row.format(*row))
    print()
    print()

    
    # behavioral characteristics
    first_bc = {}
    best_bc = {}
    for bc_name in config.feature_names:
        first_bc[bc_name] = []
        best_bc[bc_name] = []

    for r in stats[k][R]:
        for i in range(len(config.feature_names)):
            first_bc[config.feature_names[i]].append(r[FIRST][BC][i])
            best_bc[config.feature_names[i]].append(r[BEST][BC][i])

    print()
    scores = []

    for index, bc_name in enumerate(config.feature_names):
        table = []
        print(bc_name)
        table.append(build_row(FIRST, first_bc[bc_name]))
        table.append(build_row(BEST, best_bc[bc_name]))

        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))
        print()
        print()

    print()
    print('====================================================')
    print()
    print()
