from MapElites import MapElites
from Utility import *

from json import dumps as json_dumps
from os.path import join, exists
from os import mkdir
from subprocess import Popen

class BinsPerEpoch:
    def run(self, runs):
        #######################################################################
        print('Setting up data directory...')
        level_paths = [
            join(self.data_dir, 'levels_standard_n'),
            join(self.data_dir, 'levels_ngo'),
            join(self.data_dir, 'levels_gram')
        ]

        clear_directory(self.data_dir)
        for path in level_paths:
            clear_directory(path)


        #######################################################################
        print('Running Standard Operators + N-Gram')
        standard_n_counts = []
        for i in range(runs):
            standard_n_search = MapElites(
                self.start_population_size,
                self.feature_descriptors,
                self.feature_dimensions,
                self.resolution,
                self.fast_fitness,
                self.slow_fitness,
                self.minimize_performance,
                self.n_population_generator,
                self.mutator,
                self.crossover,
                self.elites_per_bin,
                rng_seed=self.seed+i
            )
            standard_n_counts.append(standard_n_search.run(self.fast_iterations, self.slow_iterations))

        print('Running NGO')
        ngo_counts = []
        for i in range(runs):
            gram_search = MapElites(
                self.start_population_size,
                self.feature_descriptors,
                self.feature_dimensions,
                self.resolution,
                self.fast_fitness,
                self.slow_fitness,
                self.minimize_performance,
                self.n_population_generator,
                self.n_mutator,
                self.n_crossover,
                self.elites_per_bin,
                rng_seed=self.seed + i
            )
            ngo_counts.append(gram_search.run(self.fast_iterations, self.slow_iterations))

        print('Running N-Grams')
        gram_counts = []
        for i in range(runs):
            only_grammar_search = MapElites(
                self.start_population_size + self.fast_iterations + self.slow_iterations,
                self.feature_descriptors,
                self.feature_dimensions,
                self.resolution,
                self.fast_fitness,
                self.slow_fitness,
                self.minimize_performance,
                self.n_population_generator,
                self.n_mutator,
                self.n_crossover,
                self.elites_per_bin,
                rng_seed=self.seed + i)

            gram_counts.append(only_grammar_search.run(0,0))

        f = open(join(self.data_dir, 'counts.json'), 'w')
        f.write(json_dumps({
            'standard_n': standard_n_counts,
            'ngo': ngo_counts,
            'grammar': gram_counts
        }))

        Popen(['python3', join('Scripts', 'build_counts_graph.py'), self.data_dir])

        #######################################################################
        print('Storing Valid Levels...')
        searches = [standard_n_search.bins, gram_search.bins, only_grammar_search.bins]

        for levels_dir, bins in zip(level_paths, searches):
            for key in bins:
                if bins[key][0][0] == 0.0:
                    with open(join(levels_dir, f'{key[0]}-{key[1]}.txt'), 'w') as f:
                        self.write_level(f, bins[key][0][1])
