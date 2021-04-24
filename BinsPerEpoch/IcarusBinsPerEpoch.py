from .BinsPerEpoch import BinsPerEpoch
from MapElites.Operators import *
from Utility.Icarus.IO import get_levels
from Utility.Icarus.Behavior import *
from Utility.Icarus.Fitness import *
from Utility.NGram import NGram

class IcarusBinsPerEpoch(BinsPerEpoch):
    def __init__(self):
        self.data_dir = f'IcarusData'

        self.start_population_size = 500
        self.fast_iterations = 50000
        self.slow_iterations = 0
        
        self.feature_names = ['density', 'leniency']
        self.feature_descriptors = [density, leniency]
        self.feature_dimensions = [[0, 0.5], [0, 0.5]] 

        self.elites_per_bin = 1
        self.resolution = 40
        
        n = 2
        self.gram = NGram(n)
        unigram = NGram(1)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)
            unigram.add_sequence(level)
        pruned = self.gram.prune() # remove dead ends from grammar

        unigram_keys = set(unigram.grammar[''].keys())
        unigram_keys.difference_update(pruned) # remove any n-gram dead ends from unigram
    
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

        self.max_path_length = 5
