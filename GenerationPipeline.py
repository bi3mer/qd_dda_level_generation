from Utility.GridTools import columns_into_grid_string
from MapElites import MapElites
from Utility import *

from subprocess import Popen
from atexit import register
from csv import writer

import sys
import os

class GenerationPipeline():
    def run(self):
        #######################################################################
        print('Setting up data directory...')
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)

        level_path = os.path.join(self.data_dir, 'levels')
        if not os.path.isdir(level_path):
            os.mkdir(level_path)
        elif len(sys.argv) == 2 and sys.argv[1] == '-o':
            data_file = os.path.join(self.data_dir, 'data.csv')
            if os.path.exists(data_file):
                os.remove(data_file)
            for filename in os.listdir(level_path):
                os.remove(os.path.join(level_path, filename))
        else:
            print(f'ERROR: Will not overwrite data. Please delete directory {level_path}')
            sys.exit(1)

        #######################################################################
        print('Starting game process...')
        self.proc = Popen(self.game_process_command)
        register(self.on_exit)

        #######################################################################
        print('Running MAP-Elites...')
        search = MapElites(
            self.start_population_size,
            self.feature_descriptors,
            self.feature_dimensions,
            self.resolution,
            self.fast_fitness,
            self.slow_fitness,
            self.minimize_performance,
            self.population_generator,
            self.mutator,
            self.crossover,
            rng_seed=self.seed
        )
        search.run(self.fast_iterations, self.slow_iterations)

        #######################################################################
        print('Storing MAP-Elites data...')
        f = open(os.path.join(self.data_dir, 'data.csv'), 'w')
        w = writer(f)
        w.writerow(self.feature_names + ['performance'])

        for i, key in enumerate(search.bins.keys()):
            w.writerow(list(key) + [search.bins[key][0]])

            level_file = open(os.path.join(level_path, f'{i}.txt'), 'w')
            level_file.write(columns_into_grid_string(search.bins[key][1]))
            level_file.close()

        f.close()

        #######################################################################
        if self.must_validate:
            print('Validating bins...')
        else:
            print('Validation bins not required.')

        #######################################################################
        print('Starting process to build MAP-Elites Graph')

        #######################################################################
        print('Building and validating bin links...')

        #######################################################################
        print('Running validation on random set of links...')


    def build_flawed_agents_links(self):
        pass

    def on_exit(self):
        self.proc.kill()
        self.proc.terminate()