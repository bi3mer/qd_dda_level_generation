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

        self.flawed_agents = [
            'no_spike',
            'no_hazard',
            'no_speed'
        ]
        
        self.start_population_size = 500
        self.fast_iterations = 100000
        self.slow_iterations = 0

        self.feature_names = ['Density', 'leniency']
        self.feature_descriptors = [density, leniency]
        self.feature_dimensions = [[0, 1.0], [0, 0.5]] 

        self.resolution = 20
        self.fast_fitness = lambda lvl: self.get_fitness(lvl, self.get_percent_playable(lvl))
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
        self.max_strand_size = 11
        self.seed = 0

        if use_standard_operators:
            mutation_values = list(unigram.grammar[''].keys())
            self.population_generator = PopulationGenerator(mutation_values, self.start_strand_size)
            self.mutator = Mutate(mutation_values, 0.02)
            self.crossover = SinglePointCrossover()
        else:
            self.population_generator = NGramPopulationGenerator(self.gram, self.start_strand_size)
            self.mutator = NGramMutate(0.02, self.gram, self.max_strand_size)
            self.crossover = NGramCrossover(self.gram, self.start_strand_size, self.max_strand_size)

        self.map_elites_config = join(self.data_dir, 'config_map_elites.json')
        self.data_file = join(self.data_dir, 'data.csv')
        self.x_label = 'Densty'
        self.y_label = 'Leniency'
        self.save_file = join(self.data_dir, 'map_elites.pdf')
        self.title = ''

        self.max_path_length = 3

    def get_percent_playable(self, level, agent=None):
        print('\n\n' + '\n'.join(columns_into_rows(level)))
        if agent == None:
            agent = FLAW_NO_FLAW

        return percent_playable(columns_into_rows(level), False, True, agent)

    def get_fitness(self, level, percent_playable, agent=None):
        bad_transitions = self.gram.count_bad_transitions(level)
        return bad_transitions + 1 - percent_playable
