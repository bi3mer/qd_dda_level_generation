from Utility.LinkerGeneration import generate_link_bfs, generate_link_mcts
from dungeongrams.dungeongrams import *
from MapElites.Operators import *
from Utility.DungeonGram.IO import get_levels
from Utility.DungeonGram.Behavior import *
from Utility.DungeonGram.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string
from dungeongrams import *

n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

print(f'pre-prune: {len(gram.grammar.keys())}')
gram.fully_connect()
print(f'post-prune: {len(gram.grammar.keys())}')
# gram.fully_connect()

# feature_dimensions = [density, leniency]
# feature_targets = [0.3, 0.2]

# __start = levels[2][-10:]
# __end = levels[1][40:]

# __start = ['-----------', 'XXXX--XXXXX', 'XXXX--XXXXX', 'XXXXX--XXXX', 'XXXXX--XXXX', '-----------', '-----------', '^^^^^-^^^^^', '^^^^^-^^^^^', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X*--------X', 'X#--------X']
# __end = ['X^^^---^^^X', 'X^^^---^^^X', 'X^^^---^^^X', 'X^^^^-^^^^X', 'X^^^^-^^^^X', 'X---------X', 'X---------X', 'XXXX---XXXX', 'XXXX---XXXX', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X---------X', 'X---------X']

# __start = ['-----------', 'XXXX--XXXXX', 'XXXX--XXXXX', 'XXXXX--XXXX', 'XXXXX--XXXX', '-----------', '-----------', '^^^^^-^^^^^', '^^^^^-^^^^^', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X*--------X', 'X#--------X']
# __end = ['--XXXX-----', '--XXXXXXXXX', '#-*XXXXXXXX', '--XXXXXXXXX', '--XXXX-----', '--XXXX-#---', '-----------', '-------XX--', '-------XX--', 'XXXXXXXX---', 'XXXXXXXX---', '-------XX--', '-------XX--', '-----------', '--XXXX-#---']

# __start = ['^^^^^^^--^^', '^^^^^^^--^^', 'XXXXXX--XXX', 'XXXXXX--XXX', '-----------', '-----------', 'X---------X', 'XX-------XX', 'XXX-----XXX', 'XXXX---XXXX', 'XXXXX-XXXXX', 'XXXXX-XXXXX', 'XX-------XX', 'XX-------XX', 'XXX-X-X-XXX']
# __end = ['--XXXX-----', '--XXXXXXXXX', '#-*XXXXXXXX', '--XXXXXXXXX', '--XXXX-----', '--XXXX-#---', '-----------', '-------XX--', '-------XX--', 'XXXXXXXX---', 'XXXXXXXX---', '-------XX--', '-------XX--', '-----------', '--XXXX-#---']

# print('BFS')
# link = generate_link_bfs(gram, __start, __end, 0)
# print(gram.sequence_is_possible(__start + link + __end))
# level = __start + ['==========='] + link + ['==========='] + __end
# print(columns_into_grid_string(level))
# print([f(link) for f in feature_dimensions])

# print()
# print('MCTS')
# link = generate_link_mcts(gram, __start, __end, feature_dimensions, feature_targets)
# level = __start + ['==========='] + link + ['==========='] + __end
# print(gram.sequence_is_possible(__start + link + __end))
# print(columns_into_grid_string(level))
# print([f(link) for f in feature_dimensions])