from Utility.GridTools import rows_into_columns, columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from Utility import Mario, DungeonGram
from shutil import copy2
import sys
import os

f = open(os.path.join(sys.argv[1], 'data.csv'))
f.readline() # remove header
bins = {}
for i, line in enumerate(f.readlines()):
    linearity, leniency, _,  = line.split(',')

    level_file = open(os.path.join(sys.argv[1], 'levels', f'{i}.txt'))
    bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
    level_file.close()

os.mkdir('level_dir')
f = open(os.path.join(sys.argv[1], 'data.csv'))
f.readline() # skip header

for i, line in enumerate(f.readlines()):
    _, _, percent_playable = line.strip().split(',')
    
    if percent_playable != '1.0':
        copy2(
            os.path.join(sys.argv[1], 'levels', f'{i}.txt'),
            os.path.join('level_dir', f'{i}.txt'))

f.close()
