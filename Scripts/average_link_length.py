from Utility.GridTools import rows_into_columns, columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from Utility.NGram import NGram
from Utility import Mario
from Utility import DungeonGram

import json
import sys
import os

if sys.argv[1] == 'mario':
    if sys.argv[2] == 'false':
        data_dir = 'MarioData_False'
    else: 
        data_dir = 'MarioData_True'
    grammar = NGram(3)

    levels = Mario.IO.get_levels()
    for level in levels:
        grammar.add_sequence(level)

elif sys.argv[1] == 'dungeon':
    if sys.argv[2] == 'false':
        data_dir = 'DungeonData_False'
    else:
        data_dir = 'DungeonData_True'

    grammar = NGram(3)

    levels = DungeonGram.IO.get_levels()
    for level in levels:
        grammar.add_sequence(level)

else:
    print(f'Unrecognized game.')
    sys.exit(-1)


f = open(os.path.join(data_dir, 'dda_graph.json'), 'r')
grid =json.load(f)
f.close()

f = open(os.path.join(data_dir, 'data.csv'), 'r')
f.readline() # get rid of header
bins = {}
for i, line in enumerate(f.readlines()):
    linearity, leniency, _ = line.split(',')

    level_file = open(os.path.join(data_dir, 'levels', f'{i}.txt'))
    bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
    level_file.close()

f.close()

link_lengths = []

for src in grid:
    neighbors = grid[src]['neighbors']
    src = bins[eval(src)]
    for tgt in neighbors:
        if neighbors[tgt] == 1.0:
            tgt = bins[eval(tgt)]

            _, length = generate_link(
                grammar,
                src,
                tgt,
                0,
                include_path_length=True
            )

            link_lengths.append(length)

print(f'min: {min(link_lengths)}')
print(f'mean: {sum(link_lengths) / len(link_lengths)}')
print(f'max: {max(link_lengths)}')
