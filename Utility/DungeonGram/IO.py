from Utility.GridTools import rows_into_columns, columns_into_grid_string
from os.path import join
from os import listdir

def get_levels():
    levels = []
    base_path = join('dungeongrams', 'train')
    for file_name in listdir(base_path):
        f = open(join(base_path, file_name))
        levels.append(rows_into_columns(f.readlines()))
        f.close()

    return levels

def write_level(f, columns):
    f.write(columns_into_grid_string(columns))
