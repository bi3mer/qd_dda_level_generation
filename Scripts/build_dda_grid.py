import matplotlib.pyplot as plt 
import networkx as nx
import json
import sys
import os


def run(algorithm_name):
    save_path = os.path.join(sys.argv[1], f'dda_grid_{algorithm_name}.pdf')
    f = open(os.path.join(sys.argv[1], f'dda_graph.json'), 'r')
    data = json.load(f)
    f.close()

    graph = nx.DiGraph()
    x_points = []
    y_points = []

    seen = set()

    for src in data:
        x,y,_ = src.split(',')
        x = int(x)
        y = int(y)

        pos = (x,y)
        if pos in seen:
            continue
        else:
            seen.add(pos)

        index = 0
        k = f'{x},{y},{index}'
        keys = []
        while k in data:
            keys.append(k)
            index += 1
            k = f'{x},{y},{index}'

        x_points.append(x)
        y_points.append(y)
        graph.add_node(pos, pos=pos)

        for k in keys:
            for dst in data[k]:
                if data[k][dst][algorithm_name]['percent_playable'] == 1.0:
                    dst_x,dst_y,_ = dst.split(',')
                    dst_pos = (int(dst_x), int(dst_y))
                    if not graph.has_node(dst_pos):
                        graph.add_node(dst_pos, pos=dst_pos)

                    graph.add_edge(pos, dst_pos)

    color_map = []
    for res in graph.in_degree():
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
    plt.figure(figsize=(15,15))
    plt.xlim(min_cor, max_cor)
    plt.ylim(min_cor, max_cor)

    nx.draw(graph, pos, node_color=color_map, node_size=60, with_labels=False, arrowsize=15) 
    # nodes = nx.draw_networkx_nodes(graph, pos, node_size=60, node_color=color_map)
    # edges = nx.draw_networkx_edges(
    #     graph,
    #     pos,
        # node_size=20,
        # arrowstyle="->",
        # arrowsize=10,
        # edge_color=edge_colors,
        # edge_cmap=cmap,
        # width=2,
    # )
    # plt.show()
    print(f'Saving to: {save_path}')
    plt.savefig(save_path, bbox_inches="tight") 

run('bfs')
run('mcts')

# nodes = set()
# for path in list(nx.bfs_edges(graph, '(0, 0)')):
#     for n in path:
#         nodes.add(n)

# file_path = os.path.join(sys.argv[1], 'info.txt')
# if os.path.exists(file_path):
#     f = open(file_path, 'a')
# else:
#     f = open(file_path, 'w')

# f.write(f'\n\nDDA Grid {sys.argv} Results\n')
# f.write(f'Connected nodes: {len(nodes)}\n')
# f.write(f'Total number of nodes: {len(graph.nodes)}\n')
# f.close()
