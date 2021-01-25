from collections import deque

import matplotlib.pyplot as plt 
import networkx as nx
import sys

from Utility.NGram import NGram
from Utility import DungeonGram
from Utility import Mario

n = 3
gram = NGram(n)
unigram = NGram(1)

if sys.argv[1] == 'mario':
    levels = Mario.get_levels()
else:
    levels = DungeonGram.get_levels()

for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

graph = nx.DiGraph()
for src in gram.grammar:
    source_list = src.split(',')
    for dst in gram.grammar[src]:
        dst_prior = deque(src, maxlen=n - 1)
        dst_prior.extend(source_list)
        dst_prior.append(dst)
        graph.add_edge(src, ','.join(dst_prior))

plt.figure(figsize=(9, 9))
nx.draw_spring(graph) 
plt.show()

for node in graph.nodes:
    if len(graph.out_edges(node)) == 0:
        print(f'{node} has no outgoing priors')