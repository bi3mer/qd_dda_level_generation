from .Extractor import *
from .config import *
from Utility.math import get_slope_and_intercept

def linearity_with_heights(heights):
    '''
    a gap is not supposed to be included in the linearity calculation. The input
    for least squares is offset to accommodate this.
    '''
    x = []
    y = []

    subtract_by = 0
    for i in range(len(heights)):
        h = heights[i]

        if h != -1:
            x.append(i - subtract_by)
            y.append(h)
        else:
            subtract_by += 1

    slope, expected = get_slope_and_intercept(x, y)
    score = 0

    for height in y:
        if height != -1:
            score += abs(expected - height)
            expected += slope

    return score

def linearity(level):
    return linearity_with_heights([min_height(col) for col in level])

def percent_linearity(level):
    return linearity(level) / max_linearity(len(level), len(level[0]))
    
def max_linearity(level_size, level_height):
    expected = level_height / 2
    h = 0
    score = 0

    for _ in range(level_size):
        score += abs(expected - h)

        if h == 0:
            h = level_height - 1
        else:
            h = 0

    return score

def contains_enemy(column):
    found_enemy = False
    for token in column:
        if token in ENEMIES:
            found_enemy = True
            break

    return found_enemy

def contains_gap(column):
    return column[0] not in SOLIDS

def percent_leniency(level):
    score = 0

    for column in level:
        if contains_enemy(column):
            score += 0.5
        
        if contains_gap(column):
            score += 0.5

    return score / len(level)
    