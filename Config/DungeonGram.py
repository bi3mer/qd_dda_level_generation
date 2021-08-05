from dungeongrams.dungeongrams import *
from Optimization.Operators import *
from Utility.DungeonGram.IO import get_levels
from Utility.DungeonGram.Behavior import *
from Utility.DungeonGram.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_rows, rows_into_columns
from Utility.LinkerGeneration import *

from dungeongrams import *

from os.path import join

name = 'DungeonGrams'
data_dir = f'DungeonData'

flawed_agents = [
    'no_spike',
    'no_hazard',
    'no_speed'
]

start_population_size = 500
iterations = 60_000

feature_names = ['Density', 'leniency']
feature_descriptors = [density, leniency]
feature_dimensions = [[0, 1.0], [0, 0.5]] 

resolution = 20
elites_per_bin = 4
fitness = lambda lvl: get_fitness(lvl, get_percent_playable(lvl))
minimize_performance = True

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

start_strand_size = 15
max_strand_size = 15

mutation_values = list(unigram_keys)
# mutate = Mutate(mutation_values, 0.02)
# crossover = SinglePointCrossover()
# population_generator = PopulationGenerator(mutation_values, start_strand_size)

mutate = NGramMutate(0.02, gram, max_strand_size)
crossover = NGramCrossover(gram, start_strand_size, max_strand_size)
population_generator = NGramPopulationGenerator(gram, start_strand_size)

map_elites_config = join(data_dir, 'config_map_elites')
data_file = join(data_dir, 'data')
x_label = 'Density'
y_label = 'Leniency'
save_file = join(data_dir, 'map_elites')
title = ''

max_path_length = 4

def get_percent_playable(level, agent=None):
    # rows = columns_into_rows(level)
    # print('\n\n' + '\n'.join(rows))
    if agent == None:
        agent = FLAW_NO_FLAW

    return percent_playable(columns_into_rows(level), False, True, agent)

def get_fitness(level, percent_playable, agent=None):
    bad_transitions = gram.count_bad_n_grams(level)
    return bad_transitions + 1 - percent_playable

def repair_level(level):
    new_level, modifications_made = repair(columns_into_rows(level), False, True, False, False)
    return rows_into_columns(new_level.split('\n')), modifications_made


    

# Linking Generated Level Segments using N-Grams
def filter_percent_playable(start, link, end):
    return get_percent_playable(start + link + end) == 1.0

def filter_link_food(start, link, end):
    return True in [dungeongrams.CHAR_FOOD in l for l in link]

link_algorithms = {
    'preferred': lambda start, end: exhaustive_link(gram, start, end, [filter_percent_playable], feature_descriptors, False),
    'shortest': lambda start, end: exhaustive_link(gram, start, end, [filter_percent_playable], feature_descriptors, True),
    'null': lambda start, end: [] if get_percent_playable(start + end) == 1.0 else None,
    'preferred+f': lambda start, end: exhaustive_link(gram, start, end, [
        filter_percent_playable,
        filter_link_food
    ], feature_descriptors, False),
}