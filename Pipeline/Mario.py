from .GenerationPipeline import GenerationPipeline

from MapElites.Operators import *
from Utility.Mario.IO import get_levels
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string

from subprocess import Popen
from pathlib import Path
from atexit import register
from shutil import rmtree
from os.path import join
from os import mkdir, remove, listdir

class Mario(GenerationPipeline):
    def __init__(self, skip_after_map_elites):
        self.data_dir = f'MarioData'
        self.skip_after_map_elites = skip_after_map_elites

        self.flawed_agents = [
            'NO_ENEMY',
            'NO_HIGH_JUMP',
            'NO_JUMP',
            'NO_SPEED'
        ]

        self.start_population_size = 500
        self.fast_iterations = 10000000
        self.slow_iterations = 10000

        self.feature_names = ['linearity', 'leniency']
        self.feature_descriptors = [percent_linearity, percent_leniency]
        self.feature_dimensions = [[0, 1], [0, 1]] 

        self.resolution = 40
        
        n = 3
        self.gram = NGram(n)
        unigram = NGram(1)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)
            unigram.add_sequence(level)

        self.fast_fitness = build_fast_fitness_function(self.gram)
        self.slow_fitness = build_slow_fitness_function(self.gram)
        self.minimize_performance = True
        
        self.start_strand_size = 25
        self.max_strand_size = 30
        self.seed = 0

        mutation_values = list(unigram.grammar[''].keys())
        self.mutator = Mutate(mutation_values, 0.02)
        self.crossover = SinglePointCrossover()
        self.population_generator = PopulationGenerator(mutation_values, self.start_strand_size)
        
        self.n_mutator = NGramMutate(0.02, self.gram, self.max_strand_size)
        self.n_crossover = NGramCrossover(self.gram, self.start_strand_size, self.max_strand_size)
        self.n_population_generator = NGramPopulationGenerator(self.gram, self.start_strand_size)

        self.map_elites_config = join(self.data_dir, 'config_map_elites.json')
        self.data_file = join(self.data_dir, 'data')
        self.x_label = 'Linearity'
        self.y_label = 'Leniency'
        self.save_file = join(self.data_dir, 'map_elites.pdf')
        self.title = ''

        self.max_path_length = 5

        # Necessary to evaluate with Robin Baumgarten agent
        print('Starting game process...')
        self.TEMP_DIR = 'TEMP_DIR'
        self.output_dir = join(self.TEMP_DIR, 'toJava')
        self.input_dir = join(self.TEMP_DIR, 'toPython')

        mkdir(self.TEMP_DIR)
        mkdir(self.output_dir)
        mkdir(self.input_dir)
        
        self.proc = Popen(['java', '-jar', 'mario_simulator.jar', self.TEMP_DIR])
        register(self.on_exit)

    def on_exit(self):
        self.proc.kill()
        self.proc.terminate()
        rmtree(self.TEMP_DIR)

    def get_percent_playable(self, level, agent=None):
        # send level file to java process. First we create a lock so Java won't 
        # read to early
        lock_file =join(self.output_dir, 'lock')
        Path(lock_file).touch()

        # write level file with the agent to be used
        if agent == None:
            f = open(join(self.output_dir, 'NO_FLAW-level.txt'), 'w')
        else:
            f = open(join(self.output_dir, f'{agent}-level.txt'), 'w')
        f.write(columns_into_grid_string(level))
        f.close()

        # remove the lock file so java can read
        remove(lock_file)

        # get results from java process
        percent_complete = -1
        while percent_complete == -1:
            files = listdir(self.input_dir)

            if len(files) == 1:
                if '_done' in files[0]:
                    percent_complete = float(files[0].split('_')[0])
                else:
                    print(f'Unknown result type: {files[0]}')
                    exit(-1)

                remove(join(self.input_dir, files[0]))
        
        return percent_complete
    
    def get_fitness(self, level, percent_playable, agent=None):
        bad_n_grams = self.gram.count_bad_n_grams(level)
        return bad_n_grams + 1 - percent_playable
