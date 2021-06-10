from dungeongrams.dungeongrams import *
from MapElites.Operators import *
from Utility.Icarus.IO import get_levels
from Utility.Icarus.Behavior import *
from Utility.Icarus.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_rows
from dungeongrams import *

from os.path import join


data_dir = f'IcarusData'

flawed_agents = []

start_population_size = 500
iterations = 10_000

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
elites_per_bin = 1
fitness = build_slow_fitness_function(gram)
minimize_performance = True
uses_separate_simulation = False

start_strand_size = 25
max_strand_size = 25
seed = 0

mutation_values = list(unigram_keys)
mutator = Mutate(mutation_values, 0.02)
crossover = SinglePointCrossover()
population_generator = PopulationGenerator(mutation_values, start_strand_size)

n_mutator = NGramMutate(0.02, gram, max_strand_size)
n_crossover = NGramCrossover(gram, start_strand_size, max_strand_size)
n_population_generator = NGramPopulationGenerator(gram, start_strand_size)

map_elites_config = join(data_dir, 'config_map_elites')
data_file = join(data_dir, 'data')
x_label = 'Density'
y_label = 'Leniency'
save_file = join(data_dir, 'map_elites')
title = ''

max_path_length = 4

def get_percent_playable(level, agent=None):
    return fitness(level)

def get_fitness(level, percent_playable, agent=None):
    bad_n_grams = gram.count_bad_n_grams(level)
    return bad_n_grams + 1 - percent_playable