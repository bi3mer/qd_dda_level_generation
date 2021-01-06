from GenerationPipeline import GenerationPipeline
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from MapElites.Operators import *
from Utility.NGram import NGram
from Utility.Mario.IO import get_levels

from os.path import join

class Mario(GenerationPipeline):
    def __init__(self):
        self.game_process_command = ['java', '-jar', 'mario_simulator.jar', 'NO_FLAW']
        self.data_dir = 'mario_data'

        self.start_population_size = 500
        self.fast_iterations = 10000000
        self.slow_iterations = 10000

        self.fast_iterations = 1000
        self.slow_iterations = 10
        
        self.feature_names = ['linearity', 'leniency']
        self.feature_descriptors = [percent_linearity, percent_leniency]
        self.feature_dimensions = [[0, 1], [0, 1]] 

        self.resolution = 50
        self.fast_fitness = fast_fitness
        self.slow_fitness = slow_fitness
        self.minimize_performance = False
        
        n = 3
        gram = NGram(n)
        levels = get_levels(join('..', 'TheVGLC', 'Super Mario Bros', 'Processed'))
        for level in levels:
            gram.add_sequence(level)

        self.start_strand_size = 25
        self.max_strand_size = 30
        self.population_generator = NGramPopulationGenerator(gram, levels[0][:n+1], self.start_strand_size)
        self.mutator = NGramMutate(0.02, gram, self.max_strand_size)
        self.crossover = NGramCrossover(gram, 0, self.max_strand_size)
        self.seed = 0

        self.must_validate = True

if __name__ == '__main__':
    pipeline = Mario()
    pipeline.run()
    pipeline.build_flawed_agents_links()
