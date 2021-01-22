from Utility.GridTools import rows_into_columns, columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from Utility import Mario, DungeonGram
from Utility.NGram import NGram
import sys
import os


f = open(os.path.join(sys.argv[1], 'data_combined.csv'))
f.readline() # remove header
bins = {}
for i, line in enumerate(f.readlines()):
    linearity, leniency, _,  = line.split(',')

    level_file = open(os.path.join(sys.argv[1], 'levels_combined', f'{linearity}_{leniency}.txt'))
    bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
    level_file.close()

f.close()

gram = NGram(3)

if 'Dungeon' in sys.argv[1]:
    levels = DungeonGram.IO.get_levels()
    for level in levels:
        gram.add_sequence(level)
elif 'Mario' in sys.argv[1]:
    levels = Mario.IO.get_levels()
    for level in levels:
        gram.add_sequence(level)
else:
    raise NameError(f'Unrecognized game: {sys.argv[1]}')

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