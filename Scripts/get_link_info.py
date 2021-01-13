import json
import sys
import os

if len(sys.argv) == 2:
    f = open(os.path.join(sys.argv[1], 'dda_graph.json'), 'r')
else:
    f = open(os.path.join(sys.argv[1], f'dda_graph_{sys.argv[2]}.json'), 'r')
    
graph = json.load(f)
f.close()

playability_scores = []

for key in graph:
    neighbors = graph[key]['neighbors']

    for dst in neighbors:
        playability_scores.append(neighbors[dst])

count = sum([score for score in playability_scores if score == 1.0])

print(f'Playable: {count}')
print(f'Total: {len(playability_scores)}')
print(f'Percent: {count / len(playability_scores)}')