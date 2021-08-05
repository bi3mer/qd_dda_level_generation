from json import load
from Config import Mario, Icarus, DungeonGram
from os.path import join

from Utility.Math import median, mean, rmse
from statistics import stdev
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
from itertools import chain, repeat

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
    if len(scores) == 0:
        return [
            name,
            'null',
            'null',
            'null',
            'null',
            'null',
        ]
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
        for alg_name in config.link_algorithms:
            bc[bc_name][alg_name] = []

    link_lengths = {}
    for alg_name in config.link_algorithms:
        link_lengths[alg_name] = []

    for k in stats:
        if k == 'target_size':
            continue
        print(f'K={k}')
        print()
        print('Links Found / runs')
        for alg_name in config.link_algorithms:
            print(f'{alg_name}: {sum([alg_name in r for r in stats[k][R]])} / {runs}')

        print()
        print('FUll Level Beatable / Links Found')
        for alg_name in config.link_algorithms:
            print(f'{alg_name}: {sum([r[alg_name][C] == 1.0 for r in stats[k][R] if alg_name in r])} / {sum([alg_name in r for r in stats[k][R]])}')

        # completability
        print()
        print()
        print('Completability')
        completability = {}
        for alg_name in config.link_algorithms:
            completability[alg_name] = []
        for r in stats[k][R]:
            for alg_name in config.link_algorithms:
                if alg_name in r:
                    completability[alg_name].append(r[alg_name][G]) 

        table = [build_row(name, completability[name]) for name in completability]

        
        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))
        print()
        print()

        # generability
        generability = {}
        for alg_name in config.link_algorithms:
            generability[alg_name] = []

        for r in stats[k][R]:
            for alg_name in config.link_algorithms:
                if alg_name in r:
                    generability[alg_name].append(r[alg_name][G]) 

        table = [build_row(name, generability[name]) for name in generability]

        print('Generability')
        format_row = "{:>9}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, table):
            print(format_row.format(*row))

        print()
        print('Usable')
        print(f'null: {sum([r["null"][C] == 1.0 for r in stats[k][R] if "null" in r and r["null"][G]])} / {sum(["null" in r for r in stats[k][R]])}')
        print()
        print()

        # BC
        for r in stats[k][R]:
            for i in range(len(config.feature_names)):
                for alg_name in config.link_algorithms:
                    if alg_name == 'null':
                        continue
                    if alg_name in r:
                        bc[config.feature_names[i]][alg_name].append(r[alg_name][BC][i])

        # link lengths
        for r in stats[k][R]:
            if alg_name == 'null':
                continue
            if alg_name in r:
                link_lengths[alg_name].extend([len(l) for l in r[alg_name][L]])

    
        print('===============================================================')
        print()

    print()
    print('===============================================================')
    print('===============================================================')

    return link_lengths, bc


def link_lengths(config, first_len, best_len, bc):
    # for index, bc_name in enumerate(config.feature_names):
    #     table = []
    #     print(bc_name)
    #     table.append(build_row(FIRST, bc[bc_name][FIRST]))
    #     table.append(build_row(BEST, bc[bc_name][BEST]))

    #     print(format_row.format(*headers))
    #     for _, row in zip(headers, table):
    #         print(format_row.format(*row))
    #     print()
    #     print()

    # print()
    # print('link Length')
    # table = []
    # table.append(build_row(FIRST, first_len))
    # table.append(build_row(BEST, best_len))

    # print(format_row.format(*headers))
    # for _, row in zip(headers, table):
    #     print(format_row.format(*row))
    print('WARNING :: link lengths not updated')


def plot_link_lengths(stuff):
    # feeling laxy, stuff is an array of tuples with (config, first_len, best_len).
    # fig, ax = plt.subplots()
    # ax.boxplot(
    #     list(chain(*[(s[1], s[2]) for s in stuff])), 
    #     labels=list(chain(*[(f'{s[0].name}\n{FIRST}', f'{s[0].name}\n{BEST}') for s in stuff])), 
    #     vert=False)

    # ax.yaxis.set_tick_params(labelsize='xx-small')
    # ax.set_title(f'Link Lengths')
    # ax.set_xlabel('Link Length')
    # plt.savefig(join('link_link_lengths.pdf'))
    # plt.close(fig)
    print('WARNING :: link lengths not updated')

# labels
# legend
# labels=[f'{con.name}\n{f_name}\n{alg}' for con, bc in zip(configs, bcs) for f_name in bc for alg in [FIRST, BEST] ],
def plot_bc(configs, bcs):
    fig, ax = plt.subplots()

    colors = {
        'preferred': '#38ba11',
        'shortest': '#9311ba',
        'preferred+f': '#ba5211'
    }

    position = 1
    data_color = []
    data = []
    pos = []

    xtick_positions = []
    xtick_names = []

    for game, bc in zip(configs, bcs):
        start = position
        for f_name in bc:
            xtick_start = position
            for alg_name in bc[f_name]:
                if alg_name == 'null':
                    continue
                
                data_color.append(colors[alg_name])
                data.append(bc[f_name][alg_name])
                pos.append(position)
                position += 1

            xtick_names.append(f_name)
            xtick_positions.append((xtick_start + position - 1)/2)

        mid = (start + position - 1) / 2
        ax.text(mid,-0.06, game.name, size=12, ha='center')
        
        position += 1

    parts = ax.violinplot(data, pos, vert=True, showmedians=True)
    for dc, b in zip(data_color, parts['bodies']):
        b.set_facecolor(dc)
    
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_names)

    # # build legend for plot by creating invisible objects
    color_names = colors.keys()
    ax.legend(
        [mpatches.Patch(color=colors[name]) for name in color_names], 
        color_names,
        prop={'size': 16})


    fig.set_size_inches(18.5, 10.5)
    # fig.set_size_inches(9, 6)
    ax.set_title(f'Behavioral Characteristic RMSE')
    ax.set_ylabel('RMSE')
    # plt.show()
    plt.savefig('link_bc.pdf')
    plt.close(fig)

m_len, m_bc = get_and_print_stats(Mario)
i_len, i_bc = get_and_print_stats(Icarus)
d_len, d_bc = get_and_print_stats(DungeonGram)

plot_link_lengths([
    (Mario, m_len),
    (Icarus, i_len,),
    (DungeonGram, d_len,),
])

plot_bc([Mario, Icarus, DungeonGram,], [m_bc, i_bc, d_bc])

