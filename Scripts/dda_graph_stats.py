import statistics
import itertools
import json
import sys
import os

def median(number_list):
    # https://www.geeksforgeeks.org/finding-mean-median-mode-in-python-without-libraries/
    number_list.sort()
    if len(number_list) % 2 == 0:
        median1 = number_list[len(number_list)//2] 
        median2 = number_list[len(number_list)//2 - 1] 
        m = (median1 + median2)/2
    else:
        m = number_list[len(number_list)//2] 

    return m

def get_stats(l):
    return [min(l), sum(l) / len(l), median(l), max(l), statistics.stdev(l)]

stats = {
    'bfs': {
        'link_lengths': [],
        'playable': [],
        'bc_targ': [],
        'bc_found': [],
        'mcts': [],
        'percent_playable': 0
    },
    'mcts': {
        'link_lengths': [],
        'playable': [],
        'bc_targ': [],
        'bc_found': [],
        'mcts': [],
        'percent_playable': 0

    }
}

f = open(os.path.join(sys.argv[1], f'dda_graph.json'), 'r')
data = json.load(f)
f.close()

for alg in ['bfs', 'mcts']:
    links = 0
    playable_links = 0

    for src in data:        
        for dst in data[src]:
            if data[src][dst][alg]['percent_playable'] != -1:
                stats[alg]['link_lengths'].append(len(data[src][dst][alg]['link']))

                if stats[alg]['link_lengths'][-1] == 0:
                    stats[alg]['bc_targ'].append(data[src][dst]['targets'])
                    stats[alg]['bc_found'].append(stats[alg]['bc_targ'][-1])
                else:
                    target = data[src][dst]['targets']
                    found = data[src][dst][alg]['behavioral_characteristics']

                    stats[alg]['bc_targ'].append(target)
                    stats[alg]['bc_found'].append(found)
                    stats[alg]['mcts'].append(sum([(target[i] - found[i])**2 for i in range(len(target))]))
                
                stats[alg]['playable'].append(data[src][dst][alg]['percent_playable'])

                links += 1
                if data[src][dst][alg]['percent_playable'] == 1.0:
                    playable_links += 1


    stats[alg]['percent_playable'] = playable_links / links


table = [[
    'min link',
    'mean link', 
    'median link',
    'max link', 
    'std link',
    
    '\nmin BC 1',
    'mean BC 1', 
    'median BC 1',
    'max BC 1', 
    'std BC 1',
    
    '\nmin BC 2',
    'mean BC 2', 
    'median BC 2',
    'max BC 2', 
    'std BC 1',

    '\nmin BC^2',
    'mean BC^2', 
    'median BC^2',
    'max BC^2', 
    'std BC^1',
    
    '\nmin playable',
    'mean playable', 
    'median playable',
    'max playable', 
    'std playable',

    '\n% beatable',
]]

for alg in ['bfs', 'mcts']:
    alg_stats = []
    alg_stats.append(get_stats(stats[alg]['link_lengths']))

    bc_difference = [[] for _ in range(len(stats[alg]['bc_targ'][0]))]
    for target, actual in zip(stats[alg]['bc_targ'], stats[alg]['bc_found']):
        for i in range(len(target)):
            bc_difference[i].append(abs(target[i] - actual[i]))

    for i, differences in enumerate(bc_difference):
        alg_stats.append(get_stats(differences))

    alg_stats.append(get_stats(stats[alg]['mcts']))
    alg_stats.append(get_stats(stats[alg]['playable']))
    table.append(list(itertools.chain(*alg_stats)))
    table[-1].append(stats[alg]['percent_playable'])

# transpose
table = [[table[j][i] for j in range(len(table))] for i in range(len(table[0]))]


print('\t\tBFS\tMCTS')
for row in table:
    print(f'{row[0]}\t{row[1]:.4f}\t{row[2]:.4f}')
