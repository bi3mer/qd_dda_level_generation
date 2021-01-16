from .config import *

def density(columns):
    num_solid_blocks = 0
    total_number_of_blocks = 0
    for col in columns:
        num_solid_blocks += col.count(SOLID_BLOCK)
        total_number_of_blocks += len(col)

    return min(0.5, num_solid_blocks / total_number_of_blocks)

def leniency(columns):
    count = 0
    for col in columns:
        if SPIKE in col or ENEMY in col:
            count += 0.5
        if SWITCH in col:
            count += 0.5

    return min(0.5, count / len(columns))
