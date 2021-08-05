from dungeongrams.dungeongrams import *
from Optimization.Operators import *
from Utility.Icarus.IO import get_levels
from Utility.Icarus.Behavior import *
from Utility.Icarus.Fitness import *
from Utility.NGram import NGram
from Utility.LinkerGeneration import *
from dungeongrams import *

from os.path import join

name = 'Icarus'

data_dir = f'IcarusData'

flawed_agents = []

start_population_size = 500
iterations = 120_000

feature_names = ['density', 'leniency']
feature_descriptors = [density, leniency]
feature_dimensions = [[0, 0.5], [0, 0.5]] 

n = 2
gram = NGram(n)
unigram = NGram(1)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

unigram_keys = set(unigram.grammar[()].keys())
pruned = gram.fully_connect() # remove dead ends from grammar
unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram

resolution = 40
elites_per_bin = 4

fitness = lambda level: get_fitness(level, get_percent_playable(level))
minimize_performance = True
uses_separate_simulation = False
is_vertical = True

start_strand_size = 25
max_strand_size = 25

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

__percent_completable = build_slow_fitness_function(gram)
def get_percent_playable(level, agent=None):
    return __percent_completable(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable

# Linking Generated Level Segments using N-Grams
def filter_percent_playable(start, link, end):
    return get_percent_playable(start + link + end) == 1.0

link_algorithms = {
    'null': lambda start, end: [] if get_percent_playable(start + end) == 1.0 else None,
    'shortest': lambda start, end: exhaustive_link(gram, start, end, [filter_percent_playable], feature_descriptors, True),
    'preferred': lambda start, end: exhaustive_link(gram, start, end, [filter_percent_playable], feature_descriptors, False),
}