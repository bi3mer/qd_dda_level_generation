from Utility.GridTools import rows_into_columns
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