from MapElites import MapElites
from Utility import *

from json import dumps as json_dumps
from os.path import join, exists
from os import mkdir
from subprocess import Popen

class BinsPerEpoch:
    def run(self, runs):
        print('Running Standard Operators')
        standard_counts = []
        for i in range(runs):
            standard_search = MapElites(
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
                self.elites_per_bin,
                rng_seed=self.seed+i
            )
            standard_counts.append(standard_search.run(self.fast_iterations, self.slow_iterations))

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

        if not exists(self.data_dir):
            mkdir(self.data_dir)

        f = open(join(self.data_dir, 'counts.json'), 'w')
        f.write(json_dumps({
            'standard': standard_counts,
            'standard_n': standard_n_counts,
            'ngo': ngo_counts
        }))

        Popen(['python3', join('Scripts', 'build_counts_graph.py'), self.data_dir])