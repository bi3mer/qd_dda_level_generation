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

seed(23141234)

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

__start = ['XbB-----------', 'X-------------', 'X-------------', 'X-------------', 'X----S--------', 'X----S--------', 'X----S--------', 'X----------?--', '--------------', 'XX-----S------', 'XXX----S------', 'XXXX----------', 'XXXXX---------', '--XX----------', '--------------', '--------------', '-----E--------', '--------S-----', '-----E--------', '-----E--------', 'XXXXX---------', '--XXX---------', '--------------', 'XXXXX---------', '--------------']
__end = ['X---X---------', '--------------', '--------------', 'X-------------', 'X-------------', 'X-------------', 'XX------------', 'XX------------', 'X-------------', 'X-------------', 'XX------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', '--------------', '-----o--------', '-----o--------', '--------------', 'X-------------', 'X-------------', 'X-------------', '--------------', '-----o--------', '-----o--------']

__start = ['X]]]>E--------', 'X-------------', 'X-------------', 'X-------------', 'XE------------', 'X-------------', 'X-------------', 'XE------------', 'XE------------', 'X-------------', 'X-------------', 'X---Q---------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X---Q---Q-----', 'X-------------', 'X-------------', 'XE------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', 'XX------------', 'XXX-----------', 'XXX-----------', '-XX-----------', '-XXX----------', '--XX----------', '--XX----------', '---XX---------', '---XX---S-----', 'X---X---S-----', 'X---X---------', '--------------', '--------------', 'X-------------', 'X-------------', 'X-------------', 'XX------------', 'XX------------', 'X-------------', 'X-------------', 'XX------------', 'X-------------', 'X-------------', 'X-------------', 'X-------------', '--------------', '-----o--------', '-----o--------', '--------------', 'X-------------', 'X-------------', 'X-------------', '--------------', '-----o--------', '-----o--------']
__end = ['XXXXX---------', '--XXX---------', '--------------', 'XXXXX---------', 'XXXXX---------', '--------------', 'XXXXXXX-------', '--------------', '--------------', 'X[[[<---------', 'X]]]>E--------', 'X-------------', 'X-------------', 'XXXX----------', '--------------', '--------------', 'XXXXX---------', '--------------', '--------------', '--------------', '--------------', 'XXXXX---------', 'XXXX----------', 'XXX-----------', 'XX------------']

assert gram.sequence_is_possible(__start)
assert gram.sequence_is_possible(__end)

link = generate_link_bfs(gram, __start, __end, 0, agent=Mario.get_percent_playable)
print(__start[0])
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])

# print('\nMCTS')
# link = generate_link_mcts(gram, __start, __end, feature_dimensions, feature_targets)
# level = __start + ['=============='] + link + ['=============='] + __end
# print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
# print(columns_into_grid_string(level))
# print([f(link) for f in feature_dimensions])

# print('\nDFS')
# link = generate_link_dfs(gram, __start, __end, 0)
# level = __start + ['=============='] + link + ['=============='] + __end
# print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
# print(columns_into_grid_string(level))
# print([f(link) for f in feature_dimensions])