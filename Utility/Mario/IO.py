from Utility.GridTools import rows_into_columns, columns_into_grid_string
import os

def get_levels():
    levels = []
    skip_levels = [
        'mario-1-2.txt', 'mario-1-3.txt', 'mario-2-1.txt', 'mario-3-3.txt', 
        'mario-4-2.txt', 'mario-4-3.txt', 'mario-5-3.txt', 'mario-6-3.txt',
        'mario-8-2.txt'
    ]

    for file_name in os.listdir('MarioLevels'):
        if file_name in skip_levels:
            continue
            
        f = open(os.path.join('MarioLevels', file_name))
        levels.append(rows_into_columns(f.readlines()))
        f.close()

    return levels

def write_level(f, columns):
    f.write(columns_into_grid_string(columns))
