from .GenerationPipeline import GenerationPipeline

from dungeongrams.dungeongrams import *
from MapElites.Operators import *
from Utility.DungeonGram.IO import get_levels
from Utility.DungeonGram.Behavior import *
from Utility.DungeonGram.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_rows
from dungeongrams import *

from os.path import join

class DungeonGram(GenerationPipeline):
    def __init__(self, use_standard_operators, skip_after_map_elites):
        self.data_dir = f'DungeonData_{use_standard_operators}'
        self.skip_after_map_elites = skip_after_map_elites
        
        self.start_population_size = 500
        self.fast_iterations = 100000
        self.slow_iterations = 0

        self.feature_names = ['Density', 'leniency']
        self.feature_descriptors = [density, leniency]
        self.feature_dimensions = [[0, 1], [0, 1]] 

        self.resolution = 50
        self.fast_fitness = self.get_percent_playable
        self.slow_fitness = None
        self.minimize_performance = False
        
        n = 3
        self.gram = NGram(n)
        unigram = NGram(1)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)
            unigram.add_sequence(level)

        self.start_strand_size = 11
        self.max_strand_size = 12
        self.seed = 0

        if use_standard_operators:
            mutation_values = list(unigram.grammar[''].keys())
            self.population_generator = PopulationGenerator(mutation_values, self.start_strand_size)
            self.mutator = Mutate(mutation_values, 0.02)
            self.crossover = TwoFoldCrossover()
        else:
            self.population_generator = NGramPopulationGenerator(self.gram, levels[0][:n+1], self.start_strand_size)
            self.mutator = NGramMutate(0.02, self.gram, self.max_strand_size)
            self.crossover = NGramCrossover(self.gram, 0, self.max_strand_size)

        self.map_elites_config = join(self.data_dir, 'config_map_elites.json')
        self.data_file = join(self.data_dir, 'data.csv')
        self.x_label = 'Densty'
        self.y_label = 'Leniency'
        self.save_file = join(self.data_dir, 'map_elites.pdf')
        self.title = ''

        self.must_validate = False
        self.max_path_length = 3

    def get_percent_playable(self, level):
        return percent_playable(columns_into_rows(level), False, True, FLAW_NO_FLAW)
