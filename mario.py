from GenerationPipeline import GenerationPipeline
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
from time import sleep

class Mario(GenerationPipeline):
    def __init__(self):
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
        levels = get_levels()
        for level in levels:
            gram.add_sequence(level)

        self.start_strand_size = 25
        self.max_strand_size = 30
        self.population_generator = NGramPopulationGenerator(gram, levels[0][:n+1], self.start_strand_size)
        self.mutator = NGramMutate(0.02, gram, self.max_strand_size)
        self.crossover = NGramCrossover(gram, 0, self.max_strand_size)
        self.seed = 0

        self.must_validate = True

        # Necessary to evaluate with Robin Baumgarten agent
        print('Starting game process...')
        self.COMMUNICATION_DIR = 'TEMP_DIR'
        rmtree(self.COMMUNICATION_DIR)
        self.output_dir = join(self.COMMUNICATION_DIR, 'toJava')
        self.input_dir = join(self.COMMUNICATION_DIR, 'toPython')

        mkdir(self.COMMUNICATION_DIR)
        mkdir(self.output_dir)
        mkdir(self.input_dir)
        
        self.proc = Popen(['java', '-jar', 'mario_simulator.jar', self.COMMUNICATION_DIR])
        register(self.on_exit)

    def on_exit(self):
        self.proc.kill()
        self.proc.terminate()
        rmtree(self.COMMUNICATION_DIR)

    def get_percent_playable(self, level):
        # send level file to java process. First we create a lock so Java won't 
        # read to early
        lock_file =join(self.output_dir, 'lock')
        Path(lock_file).touch()

        # write level file with the agent to be used
        f = open(join(self.output_dir, 'NO_FLAW-level.txt'), 'w')
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

if __name__ == '__main__':
    pipeline = Mario()
    pipeline.run()
    pipeline.build_flawed_agents_links()
