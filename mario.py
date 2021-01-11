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

class Mario(GenerationPipeline):
    def __init__(self):
        self.data_dir = 'MarioData'

        self.start_population_size = 500
        self.fast_iterations = 10000000
        self.slow_iterations = 10000

        self.feature_names = ['linearity', 'leniency']
        self.feature_descriptors = [percent_linearity, percent_leniency]
        self.feature_dimensions = [[0, 1], [0, 1]] 

        self.resolution = 50
        self.fast_fitness = fast_fitness
        self.slow_fitness = slow_fitness
        self.minimize_performance = False
        
        n = 3
        self.gram = NGram(n)
        levels = get_levels()
        for level in levels:
            self.gram.add_sequence(level)

        self.start_strand_size = 25
        self.max_strand_size = 30
        self.population_generator = NGramPopulationGenerator(self.gram, levels[0][:n+1], self.start_strand_size)
        self.mutator = NGramMutate(0.02, self.gram, self.max_strand_size)
        self.crossover = NGramCrossover(self.gram, 0, self.max_strand_size)
        self.seed = 0

        self.map_elites_config = join(self.data_dir, 'config_map_elites.json')
        self.data_file = join(self.data_dir, 'data.csv')
        self.x_label = 'Linearity'
        self.y_label = 'Leniency'
        self.save_file = join(self.data_dir, 'map_elites.pdf')
        self.title = ''

        self.must_validate = True
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
