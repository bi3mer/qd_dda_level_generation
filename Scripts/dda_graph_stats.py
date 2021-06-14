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
        'bc_found': []
    },
    'mcts': {
        'link_lengths': [],
        'playable': [],
        'bc_targ': [],
        'bc_found': [] 
    }
}

f = open(os.path.join(sys.argv[1], f'dda_graph.json'), 'r')
data = json.load(f)
f.close()

for alg in ['bfs', 'mcts']:
    for src in data:        
        for dst in data[src]:
            if data[src][dst][alg]['percent_playable'] != -1:
                stats[alg]['link_lengths'].append(len(data[src][dst][alg]['link']))

                if stats[alg]['link_lengths'][-1] == 0:
                    stats[alg]['bc_targ'].append(data[src][dst]['targets'])
                    stats[alg]['bc_found'].append(stats[alg]['bc_targ'][-1])
                else:
                    stats[alg]['bc_targ'].append(data[src][dst]['targets'])
                    stats[alg]['bc_found'].append(data[src][dst][alg]['behavioral_characteristics'])
                
                stats[alg]['playable'].append(data[src][dst][alg]['percent_playable'])


table = [[
    'min link',
    'mean link', 
    'median link',
    'max link', 
    'std link',
    
    'min BC 1',
    'mean BC 1', 
    'median BC 1',
    'max BC 1', 
    'std BC 1',
    
    'min BC 2',
    'mean BC 2', 
    'median BC 2',
    'max BC 2', 
    'std BC 1',
    
    'min playable',
    'mean playable', 
    'median playable',
    'max playable', 
    'std playable',
    
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

    alg_stats.append(get_stats(stats[alg]['playable']))
    table.append(list(itertools.chain(*alg_stats)))

# transpose
table = [[table[j][i] for j in range(len(table))] for i in range(len(table[0]))]


print('\t\ttBFS\tMCTS')
for row in table:
    print(f'{row[0]}\t{row[1]:.4f}\t{row[2]:.4f}')
