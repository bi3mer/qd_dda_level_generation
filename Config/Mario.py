from Optimization.Operators import *
from Utility.Mario.IO import get_levels
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from Utility.NGram import NGram
from Utility.LinkerGeneration import *

from os.path import join

name = 'Mario'

data_dir = f'MarioData'

flawed_agents = [
    'NO_ENEMY',
    'NO_HIGH_JUMP',
    'NO_JUMP',
    'NO_SPEED'
]

start_population_size = 500
iterations = 80_000

feature_names = ['linearity', 'leniency']
feature_descriptors = [percent_linearity, percent_leniency]
feature_dimensions = [[0, 1], [0, 1]] 

elites_per_bin = 4
resolution = 40

uses_separate_simulation = False
is_vertical = False

n = 3
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

unigram_keys = set(unigram.grammar[()].keys())
pruned = gram.fully_connect() # remove dead ends from grammar
unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram

# fitness = summerville_fitness(gram)
minimize_performance = True

start_strand_size = 25
max_strand_size = 25

# mutation_values = list(unigram_keys)
# mutate = Mutate(mutation_values, 0.02)
# crossover = SinglePointCrossover()
# population_generator = PopulationGenerator(mutation_values, start_strand_size)

mutate = NGramMutate(0.02, gram, max_strand_size)
crossover = NGramCrossover(gram, start_strand_size, max_strand_size)
population_generator = NGramPopulationGenerator(gram, start_strand_size)

map_elites_config = join(data_dir, 'config_map_elites')
data_file = join(data_dir, 'data')
x_label = 'Linearity'
y_label = 'Leniency'
save_file = join(data_dir, 'map_elites')
title = ''

max_path_length = 5

def get_percent_playable(level, agent=None):
    return percent_playable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))

# Linking Generated Level Segments using N-Grams
def filter_percent_playable(start, link, end):
    return get_percent_playable(start + link + end) == 1.0

FILTERS = [filter_percent_playable]
LINKERS = {
    'null': lambda start, end: [] if get_percent_playable(start + end) == 1.0 else None,
    'shortest': lambda start, end: exhaustive_link(gram, start, end, FILTERS, feature_descriptors, True),
    'BC-match': lambda start, end: exhaustive_link(gram, start, end, FILTERS, feature_descriptors, False),
}

# FOr now, let's not bother with Infinite Mario Bros.
# Necessary to evaluate with Robin Baumgarten agent
# print('Starting game process...')
# TEMP_DIR = 'TEMP_DIR'
# output_dir = join(TEMP_DIR, 'toJava')
# input_dir = join(TEMP_DIR, 'toPython')

# mkdir(TEMP_DIR)
# mkdir(output_dir)
# mkdir(input_dir)

# def on_exit():
#     proc.kill()
#     proc.terminate()
#     rmtree(TEMP_DIR)

# proc = Popen(['java', '-jar', 'mario_simulator.jar', TEMP_DIR])
# register(on_exit)

# def get_percent_playable(level, agent=None):
#     # send level file to java process. First we create a lock so Java won't 
#     # read to early
#     lock_file =join(output_dir, 'lock')
#     Path(lock_file).touch()

#     # write level file with the agent to be used
#     if agent == None:
#         f = open(join(output_dir, 'NO_FLAW-level.txt'), 'w')
#     else:
#         f = open(join(output_dir, f'{agent}-level.txt'), 'w')
#     f.write(columns_into_grid_string(level))
#     f.close()

#     # remove the lock file so java can read
#     remove(lock_file)

#     # get results from java process
#     percent_complete = -1
#     while percent_complete == -1:
#         files = listdir(input_dir)

#         if len(files) == 1:
#             if '_done' in files[0]:
#                 percent_complete = float(files[0].split('_')[0])
#             else:
#                 print(f'Unknown result type: {files[0]}')
#                 exit(-1)

#             remove(join(input_dir, files[0]))
    
#     return percent_complete

# def get_fitness(level, percent_playable, agent=None):
#     bad_n_grams = gram.count_bad_n_grams(level)
#     return bad_n_grams + 1 - percent_playable
