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
    for dst in gram.grammar[src]:
        graph.add_edge(src, dst)

plt.figure(figsize=(9, 9))
nx.draw_spring(graph) 
plt.show()