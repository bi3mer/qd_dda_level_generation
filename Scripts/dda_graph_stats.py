import statistics
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

def print_list_stats(l, title):
    print(title)
    print(f'min: {min(l)}')
    print(f'mean: {sum(l) / len(l)}')
    print(f'median: {median(l)}')
    print(F'max: {max(l)}')
    print(f'std: {statistics.stdev(l)}')
    print()


f = open(os.path.join(sys.argv[1], f'dda_graph.json'), 'r')
data = json.load(f)
f.close()

for alg in ['bfs', 'mcts']:
    print(alg.upper())
    
    link_lengths = []
    target_bc = []
    alg_bc = []
    playable = []
    for src in data:        
        for dst in data[src]:
            link_lengths.append(len(data[src][dst][alg]['link']))

            if link_lengths[-1] == 0:
                target_bc.append(data[src][dst]['targets'])
                alg_bc.append(target_bc[-1])
            elif data[src][dst][alg]['percent_playable'] == -1:
                # skip since no valid link was found
                pass
            else:
                target_bc.append(data[src][dst]['targets'])
                alg_bc.append(data[src][dst][alg]['behavioral_characteristics'])

            playable.append(data[src][dst][alg]['percent_playable'])
    
    print_list_stats(link_lengths, 'Links')

    print('Behavioral Characteristics')
    bc_difference = [[] for _ in range(len(target_bc[0]))]
    for target, alg in zip(target_bc, alg_bc):
        for i in range(len(target)):
            bc_difference[i].append(abs(target[i] - alg[i]))

    for i, differences in enumerate(bc_difference):
        print_list_stats(differences, f'BC {i}:')

    print_list_stats(playable, 'Playable')

    print()
    print()