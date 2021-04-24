from .GenerationPipeline import GenerationPipeline

from dungeongrams.dungeongrams import *
from MapElites.Operators import *
from Utility.Icarus.IO import get_levels
from Utility.Icarus.Behavior import *
from Utility.Icarus.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_rows
from dungeongrams import *

from os.path import join

class Icarus(GenerationPipeline):
    def __init__(self, skip_after_map_elites):
        self.data_dir = f'IcarusData'
        self.skip_after_map_elites = skip_after_map_elites

        self.flawed_agents = []
        
        self.start_population_size = 500
        self.fast_iterations = 1000
        self.slow_iterations = 0

        self.feature_names = ['density', 'leniency']
        self.feature_descriptors = [density, leniency]
        self.feature_dimensions = [[0, 0.5], [0, 0.5]] 

        n = 2
        self.gram = NGram(n)
        unigram = NGram(1)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)
            unigram.add_sequence(level)
        pruned = self.gram.prune()

        unigram_keys = set(unigram.grammar[''].keys())
        unigram_keys.difference_update(pruned)

        self.resolution = 40
        self.elites_per_bin = 1
        self.fast_fitness = build_slow_fitness_function(self.gram)
        self.slow_fitness = None
        self.minimize_performance = True
        
        self.start_strand_size = 25
        self.max_strand_size = 25
        self.seed = 0

        mutation_values = list(unigram_keys)
        self.mutator = Mutate(mutation_values, 0.02)
        self.crossover = SinglePointCrossover()
        self.population_generator = PopulationGenerator(mutation_values, self.start_strand_size)

        self.n_mutator = NGramMutate(0.02, self.gram, self.max_strand_size)
        self.n_crossover = NGramCrossover(self.gram, self.start_strand_size, self.max_strand_size)
        self.n_population_generator = NGramPopulationGenerator(self.gram, self.start_strand_size)

        self.map_elites_config = join(self.data_dir, 'config_map_elites')
        self.data_file = join(self.data_dir, 'data')
        self.x_label = 'Density'
        self.y_label = 'Leniency'
        self.save_file = join(self.data_dir, 'map_elites')
        self.title = ''

        self.max_path_length = 4

    def get_percent_playable(self, level, agent=None):
        return self.fast_fitness(level)

    def get_fitness(self, level, percent_playable, agent=None):
        return self.fast_fitness(level)
