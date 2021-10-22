from Utility.DungeonGram.Behavior import leniency
from Utility.LinkerGeneration import *
from dungeongrams.dungeongrams import *
from Optimization.Operators import *
from Utility.Mario.IO import get_levels
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string, columns_into_rows
from dungeongrams import *
from random import seed
from Config import Mario


n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

gram.fully_connect()

# feature_dimensions = [density, leniency]  
feature_dimensions = [linearity, leniency]
feature_targets = [0.3, 0.2]
feature_targets = [0.23636363636363636, 0.14444444444444443]

__start = levels[-1][15:25]
__end = levels[-1][15:25]

__start = levels[-1][15:25]
__end = levels[0][15:25]

__start = ['XXX-----------', 'X-------------', 'XE------------', 'XE------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------S-----', 'X---S---S-----', 'X-------S-----', 'X--E----S-----', 'X-------S-----', 'X-------------', 'X-------------', 'X----o--------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', '--------------', 'X-------------']
__end = ['--------------', '--------------', 'XXXX----------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'XXXXX---------', 'X-------S-----', 'X-------S-----', 'X---S---S-----', 'XE------S-o---', 'X-------------', 'X-------------', 'X-------S-----', 'X-------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----']

__start = ['--------------', '--------------', 'XXXX----------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'XXXXX---------', 'X-------S-----', 'X-------S-----', 'X---S---S-----', 'XE------S-o---', 'X-------------', 'X-------------', 'X-------S-----', 'X-------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----']
__end = ['--------------', '--------------', 'XXXX----------', 'X-------------', 'X-------------', 'X-------S-----', 'X-------S-----', '--------S-----', '--------S-----', '--------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'XX------------', 'XXX-----------', 'XXX-----------', '-XX-----------', '-XXX----------', '--XX----------', '--XX----------', '---XX---------', '---XX---S-----']

__start = ['--------------', '--------------', 'X-------------', '--------------', '--------------', 'X-------------', 'X-------------', 'X-------S-----', 'X-------S-----', 'X-------------', 'X-------------', '--------------', '--------------', '--------------', '-----o--------', '-----o--------', '--------------', 'X-------------', 'X-------------', 'XX------------', 'XXX-----------', 'XXX-----------', '-XX-----------', '-XXX----------', '--XX----------']
__end = ['------S-------', '----S---------', '--S-S---------', '--S---o-------', '--S-----------', 'X-------------', 'X-------------', 'X-------S-----', 'X-------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------S-----', '--------------', 'X-------------', '--------------', '--------------', '-----E--------', '--------S-----', '-----E--------', '-----E--------']p

assert gram.sequence_is_possible(__start)
assert gram.sequence_is_possible(__end)

print('Prior BFS')
link = generate_link(gram, __start, __end, 1, agent=Mario.get_percent_playable)
assert gram.sequence_is_possible(link)
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])
print(f'playability: {Mario.get_percent_playable(__start + link + __end)}')
print(len(link))

MAX_LENGTH = 10
print('\nPrior Exhaustive True')
link = exhaustive_link(gram, __start, __end, Mario.get_percent_playable, Mario.feature_descriptors, True, max_length=MAX_LENGTH)
assert gram.sequence_is_possible(link)
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])
print(f'playability: {Mario.get_percent_playable(__start + link + __end)}')
print(len(link))

print('\nPrior Exhaustive False')
link = exhaustive_link(gram, __start, __end, Mario.get_percent_playable, Mario.feature_descriptors, False, max_length=MAX_LENGTH)
assert gram.sequence_is_possible(link)
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])
print(f'playability: {Mario.get_percent_playable(__start + link + __end)}')
print(len(link))


