from Utility.Mario import config
from Config import Mario
from Utility.LinkerGeneration import *

start = [
    'XXX-----------',
    'XXXX----------',
    'XXXXX---------',
    'XXXXXX--------',
    'XXXXXXX-------',
    'X-------------'
]

end = [
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    'X-------------',
    '--------------',
    'X-------------',
]


bfs_link = generate_link_bfs(Mario.gram, start, end, 0)
mcts_link = generate_link_mcts(Mario.gram, start, end, Mario.feature_descriptors, [0.3, 0.2])

print(Mario.gram.sequence_is_possible(start + bfs_link + end), bfs_link)
print(Mario.gram.sequence_is_possible(start + mcts_link + end), mcts_link)
