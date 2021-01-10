from Utility.GridTools import rows_into_columns, columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from Utility.Mario.IO import get_levels
from Utility.NGram import NGram
import sys
import os

f = open(os.path.join(sys.argv[1], 'data.csv'))
f.readline() # remove header
bins = {}
for i, line in enumerate(f.readlines()):
    linearity, leniency, _, __ = line.split(',')

    level_file = open(os.path.join(sys.argv[1], 'levels', f'{i}.txt'))
    bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
    level_file.close()

f.close()

gram = NGram(3)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)

path = eval(sys.argv[2])
level = None
for point in path:
    if level == None:
        level = bins[point]
    else:
        level = generate_link(
            gram, 
            level, 
            bins[point], 
            0)

print(columns_into_grid_string(level))