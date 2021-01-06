from . import config

def heights(column):
    heights = []
    for h in reversed(range(len(column))):
        if column[h] in config.SOLIDS:
            heights.append(h)

    return heights

def max_height(column):
    '''
    -1 means that there is no solid found.
    '''
    found = False
    height = len(column) - 1
    while height >= 0:
        if column[height] in config.SOLIDS:
            found = True
            break

        height -= 1
    
    return height if found else -1

def min_height(column):
    '''
    -1 means that there is no solid found.
    '''
    found = False
    height = 0
    while height <= len(column) - 1:
        if column[height] in config.SOLIDS:
            found = True
        elif found:
            break

        height += 1
    
    return height - 1 if found else -1

def contains_enemy(column):
    found_enemy = False
    for token in column:
        if token in config.ENEMIES:
            found_enemy = True
            break

    return found_enemy

def contains_gap(column):
    return column[0] not in config.SOLIDS

def column_to_leniency_score(column):
    score = 0
    
    if contains_enemy(column):
        score += 0.5
    
    if contains_gap(column):
        score += 0.5

    return score