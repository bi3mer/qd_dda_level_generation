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
            for alg_name in config.link_algorithms:
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

def plot_link_lengths(configs, lengths):
    colors = {
        'BC-match': '#38ba11',
        'shortest': '#9311ba',
        'BC-match-f': '#ba5211'
    }

    data_color = []
    data = []
    pos = []
    
    fig, ax = plt.subplots()
    position = 1
    for game, game_lengths in zip(configs, lengths):
        start = position
        for alg_name in game_lengths:
            if alg_name == 'null':
                continue
            
            data_color.append(colors[alg_name])
            data.append(game_lengths[alg_name])
            pos.append(position)
            position += 1

        mid = (start + position - 1) / 2
        ax.text(mid,-0.6, game.name, size=14, ha='center')
        position += 1

    parts = ax.violinplot(data, pos, vert=True, showmedians=True)
    for dc, b in zip(data_color, parts['bodies']):
        b.set_facecolor(dc)

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off

    # # build legend for plot by creating invisible objects
    color_names = colors.keys()
    legend = ax.legend(
        [mpatches.Patch(color=colors[name]) for name in color_names], 
        color_names,
        bbox_to_anchor=(1.05, 1), 
        loc='upper left',
        prop={'size': 12})
    
    ax.set_title(f'Link Lengths')
    fig.set_size_inches(9, 6)
    plt.savefig(
        join('link_lengths.pdf'), 
        bbox_extra_artists=(legend,),
        bbox_inches='tight',
        pad_inches=0.3)
    # plt.show()
    plt.close(fig)

def plot_bc_dual(configs, bcs):
    fig, ax = plt.subplots()

    colors = {
        'BC-match': '#38ba11',
        'shortest': '#9311ba',
        'BC-match-f': '#ba5211'
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
        ax.text(mid,-0.1, game.name, size=12, ha='center')
        
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
    plt.savefig('link_bc.pdf', bbox_inches='tight',
        pad_inches=0.3)
    plt.close(fig)

def plot_bc_singular(configs, bcs):
    fig, ax = plt.subplots()

    colors = {
        'BC-match': '#38ba11',
        'shortest': '#9311ba',
        'BC-match-f': '#ba5211'
    }

    position = 1
    data_color = []
    data = []
    pos = []


    for game, bc in zip(configs, bcs):
        start = position
        for alg_name in game.link_algorithms:
            if alg_name == 'null':
                    continue

            alg_data = []
            for bc_name in bc:
                alg_data.extend(bc[bc_name][alg_name])

            data_color.append(colors[alg_name])
            data.append(alg_data)
            pos.append(position)
            position += 1


        mid = (start + position - 1) / 2
        ax.text(mid,-0.1, game.name, size=12, ha='center')
        
        position += 1

    parts = ax.violinplot(data, pos, vert=True, showmedians=True)
    for dc, b in zip(data_color, parts['bodies']):
        b.set_facecolor(dc)
    
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
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
        
    plt.savefig('link_bc_singular.pdf', bbox_inches='tight',
        pad_inches=0.3)
    plt.close(fig)

m_len, m_bc = get_and_print_stats(Mario)
i_len, i_bc = get_and_print_stats(Icarus)
d_len, d_bc = get_and_print_stats(DungeonGram)

plot_link_lengths(
    [Mario, Icarus, DungeonGram],
    [m_len, i_len, d_len])

plot_bc_dual([Mario, Icarus, DungeonGram,], [m_bc, i_bc, d_bc])
plot_bc_singular([Mario, Icarus, DungeonGram,], [m_bc, i_bc, d_bc])

