from Utility.DungeonGram.Behavior import leniency
from Utility.LinkerGeneration import *
from dungeongrams.dungeongrams import *
from Optimization.Operators import *
from Utility.DungeonGram.IO import get_levels
from Utility.DungeonGram.Behavior import *
from Utility.DungeonGram.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string, columns_into_rows
from dungeongrams import *
from random import seed

seed(23141234)

n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

gram.fully_connect()

feature_dimensions = [density, leniency]
# feature_dimensions = [linearity, leniency]
feature_targets = [0.3, 0.2]
feature_targets = [0.23636363636363636, 0.14444444444444443]

__start = levels[0][10:20]
__end = levels[4][10:20]

__start = ['^^^^^^^--^^', '^^^^^^^--^^', '^^^^^^^--^^', '^^^^^^--^^^', '^^^^^^--^^^', '^^^^^--^^^^', '^^^^^--^^^^', '-----------', '-----------', '-----------', '-----------', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX']
__end = ['^---XXX---^', '^---------^', '^---------^', '-----------', '-----------', 'X-XXX*XXX-X', '---XX#XX---', '----XXX----', '-----------', '-----------', 'XXXX-XXXXXX', 'XXXX-XXXXXX', 'XXXX---XXXX', 'XXXX---XXXX', 'XXXX--*XXXX']

print('BFS')
link = generate_link_bfs(gram, __start, __end, 0)
print(__start[0])
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])

print('\nMCTS')
link = generate_link_mcts(gram, __start, __end, feature_dimensions, feature_targets)
level = __start + ['=============='] + link + ['=============='] + __end
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])

print('\nDFS')
link = generate_link_dfs(gram, __start, __end, 0)
level = __start + ['=============='] + link + ['=============='] + __end
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])