from Utility.GridTools import columns_into_rows
from Utility import PlatformerRepair
from Config import Mario
from Utility import columns_into_rows

columns_impossible_jump = [
    'X-------------',
    'X-------------',
    'X-------------',
    '--------------',
    '--------------',
    '--------------',
    '--------------',
    '--------------',
    '--------------',
    '--------------',
    'X-------------',
    'X-------------',
    'X-------------'
]

columns = [
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------'
]

print(PlatformerRepair.findPaths(Mario.SOLIDS, Mario.JUMPS, True, columns_into_rows(columns), (-1, -1, 1, len(columns) - 2, -1, len(columns) - 2), False))