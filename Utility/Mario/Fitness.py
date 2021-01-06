from .Extractor import max_height, heights as col_heights
from .SummervilleAgent import percent_completable

def percent_playable(columns, start_position):
    '''
    This uses an A* agent to tell if a level is playable. It should be pretty
    close to perfect.
    '''
    return percent_completable(10, start_position, (columns))

def naive_percent_playable(columns):
    '''
    This uses an approximation. It is not perfect. It is meant to be fast. Use
    percent_playable for a perfect score.
    '''
    column_iter = iter(columns)
    col = next(column_iter)

    current_height = max_height(col)
    gaps_seen = 0 if current_height != -1 else 1

    for i, col in enumerate(columns):
        heights = col_heights(col)

        if len(heights) == 0:
            gaps_seen += 1

            if gaps_seen > 6:
                break
        else:
            valid_height = -1
            for h in heights:
                if not (h > current_height + 4):
                    valid_height = h
                    break

            if valid_height == -1:
                current_height = valid_height
                gaps_seen += 1
            else:
                current_height = heights[0]
                gaps_seen = 0

    if i == len(columns) - 1:
        return 1.0 # remove rounding error for unit tests

    return i / len(columns)

def slow_fitness(columns):
    columns.insert(0, 'X-------------')
    columns.insert(0, 'X-------------')
    fitness = percent_playable(columns, (1, 1, -1),)
    columns.pop(0)
    columns.pop(0)

    return fitness

def fast_fitness(columns):
    columns.insert(0, 'X-------------')
    columns.insert(0, 'X-------------')
    fitness = naive_percent_playable(columns)
    columns.pop(0)
    columns.pop(0)

    return fitness