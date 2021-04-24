import os

def get_levels():
    levels = []

    for file_name in os.listdir('IcarusLevels'):
        with open(os.path.join('IcarusLevels', file_name)) as f:
            levels.append([l.strip() for l in reversed(f.readlines())])

    return levels
