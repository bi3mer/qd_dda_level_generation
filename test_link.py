from Utility.LinkerGeneration import *
# from dungeongrams.dungeongrams import *
from MapElites.Operators import *
from Utility.Icarus.IO import get_levels
from Utility.Icarus.Behavior import *
from Utility.Icarus.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string, columns_into_rows
# from dungeongrams import *

n = 2
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

gram.fully_connect()

# feature_dimensions = [density, leniency]
feature_targets = [0.3, 0.2]

__start = levels[-5][10:20]
__end = levels[-2][20:30]


# __start = ['-----------', 'XXXX--XXXXX', 'XXXX--XXXXX', 'XXXXX--XXXX', 'XXXXX--XXXX', '-----------', '-----------', '^^^^^-^^^^^', '^^^^^-^^^^^', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X*--------X', 'X#--------X']
# __end = ['X^^^---^^^X', 'X^^^---^^^X', 'X^^^---^^^X', 'X^^^^-^^^^X', 'X^^^^-^^^^X', 'X---------X', 'X---------X', 'XXXX---XXXX', 'XXXX---XXXX', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X---------X', 'X---------X']

# __start = ['-----------', 'XXXX--XXXXX', 'XXXX--XXXXX', 'XXXXX--XXXX', 'XXXXX--XXXX', '-----------', '-----------', '^^^^^-^^^^^', '^^^^^-^^^^^', '-----------', '-----------', 'XXXX---XXXX', 'XXXX---XXXX', 'X*--------X', 'X#--------X']
# __end = ['--XXXX-----', '--XXXXXXXXX', '#-*XXXXXXXX', '--XXXXXXXXX', '--XXXX-----', '--XXXX-#---', '-----------', '-------XX--', '-------XX--', 'XXXXXXXX---', 'XXXXXXXX---', '-------XX--', '-------XX--', '-----------', '--XXXX-#---']

# __start = ['^^^^^^^--^^', '^^^^^^^--^^', 'XXXXXX--XXX', 'XXXXXX--XXX', '-----------', '-----------', 'X---------X', 'XX-------XX', 'XXX-----XXX', 'XXXX---XXXX', 'XXXXX-XXXXX', 'XXXXX-XXXXX', 'XX-------XX', 'XX-------XX', 'XXX-X-X-XXX']
# __end = ['--XXXX-----', '--XXXXXXXXX', '#-*XXXXXXXX', '--XXXXXXXXX', '--XXXX-----', '--XXXX-#---', '-----------', '-------XX--', '-------XX--', 'XXXXXXXX---', 'XXXXXXXX---', '-------XX--', '-------XX--', '-----------', '--XXXX-#---']

# __start = [
#     '#-------##-----#',
#     '#-------#####--#',
#     '#-----------#--#',
#     '##----------#--#',
#     '#########---#--#',
#     '-------##---#T--',
#     '-------##---#---',
#     '-------##TT-#---',
#     '##-----##---####',
#     '----TT---T------',
#     '----------------',
#     '##----------####',
#     '######------####',
#     '----------------',
#     '----------------',
#     '#HHH#--#HHHHHH##',
#     '#####--########-',
# ]

# __end = [
#     '###------------#',
#     '###---------T--#',
#     '----------------',
#     'TTTTT-TTTT-----#',
#     '---------------#',
#     '---#D----------#',
#     '#--#D----------#',
# ]

# __start = ['-########--#####', '##HHHHHH#--#HHH#', '----------------', '----------------', '####------######', '####----------##', '----------------', '------T---TT----', '####---##-----##', '---#-TT##-------', '---#---##-------', '--T#---##-------', '#--#---#########', '#--#----------##', '#--#-----------#', '#--#####-------#', '#-----##-------#']
# __end =   ['#----------D#--#', '#----------D#---', '#---------------', '#-----TTTT-TTTTT', '----------------', '#--T---------###', '#------------###']

# __start = ['#---############', '#------#---#--D#', '#-------------D#', '#-------------D#', '#------------###', '####---#####-###', '################', '#####---########', '#D-------------#', '##----------TTTT', '##-------------#', '#########------#', '#--------------#', '#--------------#', '#MMMMMMMMMMMMMM#', '#H-----------H##']
# __end = ['#-T------------#', '#------#-------#', '#--------------#', '#MMMMMMMMMMMMMM#', '----------------', '---------------#', '-------TTTT-----', '-------####-----']

# __start = list(reversed(__start))
# __end = list(reversed(__end))



print('BFS')
link = generate_link_bfs(gram, __start, __end, 0)
print(link)
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
print(f'possible: {gram.sequence_is_possible(link)}')
# level = __start + ['==========='] + link + ['==========='] + __end
# print(columns_into_grid_string(columns_into_rows(level)))
# print([f(link) for f in feature_dimensions])

# print()
# print('MCTS')
# link = generate_link_mcts(gram, __start, __end, feature_dimensions, feature_targets)
# level = __start + ['==========='] + link + ['==========='] + __end
# print(gram.sequence_is_possible(__start + link + __end))
# print(columns_into_grid_string(level))
# print([f(link) for f in feature_dimensions])

print('DFS')
link = generate_link_dfs(gram, __start, __end, 0)
print(link)
print(f'possible: {gram.sequence_is_possible(__start + link + __end)}')
print(f'possible: {gram.sequence_is_possible(link)}')
# level = __start + ['==========='] + link + ['==========='] + __end
# print(columns_into_grid_string(columns_into_rows(level)))
# print([f(link) for f in feature_dimensions])