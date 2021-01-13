import matplotlib.pyplot as plt 
import networkx as nx
import json
import sys
import os

if len(sys.argv) == 2:
    save_path = os.path.join(sys.argv[1], 'dda_grid.pdf')
    f = open(os.path.join(sys.argv[1], 'dda_graph.json'), 'r')
else:
    save_path = os.path.join(sys.argv[1], f'dda_grid_{sys.argv[2]}.pdf')
    f = open(os.path.join(sys.argv[1], f'dda_graph_{sys.argv[2]}.json'), 'r')
data =json.load(f)
f.close()

graph = nx.DiGraph()
x_points = []
y_points = []

for src in data:
    x,y = src[1:-1].split(',')
    x_points.append(int(x))
    y_points.append(int(y))
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


min_cor = min(min(x_points), min(y_points)) - 1
max_cor = max(max(x_points), max(y_points)) + 1

pos = nx.get_node_attributes(graph, 'pos')
plt.figure(figsize=(12,12))
plt.xlim(min_cor, max_cor)
plt.ylim(min_cor, max_cor)

nx.draw(graph, pos, node_color=color_map, node_size=10, with_labels=False, arrowsize=5) 
plt.savefig(save_path, bbox_inches="tight") 

nodes = set()
for path in list(nx.bfs_edges(graph, '(0, 0)')):
    for n in path:
        nodes.add(n)

print(f'Connected nodes: {len(nodes)}')
print(f'total number of nodes: {len(graph.nodes)}')
