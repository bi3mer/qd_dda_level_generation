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

__start = levels[6][10:15]
__end = levels[4][30:40]


print('BFS')
link = generate_link_bfs(gram, __start, __end, 0)
print(__start[0])
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
level = __start + ['=============='] + link + ['=============='] + __end
print(columns_into_grid_string(level))
print([f(link) for f in feature_dimensions])

print('\nMCTS')
link = generate_link_mcts(gram, __start, __end, feature_dimensions, [0.3, 0.2])
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