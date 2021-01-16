from shutil import copy2
import sys
import os

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
