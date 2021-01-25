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
    def __init__(self, skip_after_map_elites):
        self.data_dir = f'DungeonData'
        self.skip_after_map_elites = skip_after_map_elites

        self.flawed_agents = [
            'no_spike',
            'no_hazard',
            'no_speed'
        ]
        
        self.start_population_size = 50
        self.fast_iterations = 100
        self.slow_iterations = 0

        self.feature_names = ['Density', 'leniency']
        self.feature_descriptors = [density, leniency]
        self.feature_dimensions = [[0, 1.0], [0, 0.5]] 

        self.resolution = 20
        self.fast_fitness = lambda lvl: self.get_fitness(lvl, self.get_percent_playable(lvl))
        self.slow_fitness = None
        self.minimize_performance = True
        
        n = 3
        self.gram = NGram(n)
        unigram = NGram(1)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)
            unigram.add_sequence(level)

        self.start_strand_size = 15
        self.max_strand_size = 15
        self.seed = 0

        mutation_values = list(unigram.grammar[''].keys())
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
        rows = columns_into_rows(level)
        print('\n\n' + '\n'.join(rows))
        if agent == None:
            agent = FLAW_NO_FLAW

        return percent_playable(rows, False, True, agent)

    def get_fitness(self, level, percent_playable, agent=None):
        bad_transitions = self.gram.count_bad_n_grams(level)
        return bad_transitions + 1 - percent_playable
