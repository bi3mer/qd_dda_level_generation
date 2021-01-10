import matplotlib.pyplot as plt 
import networkx as nx
import json
import sys
import os


f = open(sys.argv[1], 'r')
data =json.load(f)
f.close()

graph = nx.DiGraph()

for src in data:
    x,y = src[1:-1].split(',')
    graph.add_node(src, pos=(int(x), int(y)))

for src in data:
    neighbors = data[src]['neighbors']
    for dst in data[src]['neighbors']:
        if neighbors[dst] == 1:
            graph.add_edge(src, dst)

color_map = []
for i, res in enumerate(graph.in_degree()):
    node_key, in_edges = res
    if in_edges == 0:
        color_map.append('gray')
    elif graph.out_degree(node_key) == 0:
        color_map.append('green')
    else:
        color_map.append('brown')

pos = nx.get_node_attributes(graph, 'pos')
plt.figure(figsize=(10,10))
nx.draw(graph, pos, node_color=color_map, node_size=10, with_labels=False, arrowsize=5) 
plt.savefig(os.path.join(sys.argv[2], 'dda_grid.pdf'), bbox_inches="tight") 
