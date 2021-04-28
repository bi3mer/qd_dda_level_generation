from MapElites import MapElites
from Utility import *

from json import dumps as json_dumps
from os.path import join, exists
from os import mkdir
from subprocess import Popen

class BinsPerEpoch:
    def run_generator(self, runs, build_map_elites, fast_iterations, slow_iterations, name):
        bins = {}
        counts = []

        for i in range(runs):
            print(f'{name}: {i}/{runs}')

            search = build_map_elites(i)
            counts.append(search.run(fast_iterations, slow_iterations))

            for k in search.bins:
                if search.bins[k][0][0] == 0.0:
                    key = str(k)
                    if key in bins:
                        bins[key] += 1
                    else:
                        bins[key] = 1
        
        return bins, counts, search

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
        builder = lambda i: MapElites(
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
        so_bins, so_counts, so_search = self.run_generator(
            runs, 
            builder, 
            self.fast_iterations, 
            self.slow_iterations, 
            'SO'
        )

        print('Running NGO')
        builder = lambda i: MapElites(
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
        ng_bins, ng_counts, ng_search  = self.run_generator(
            runs, 
            builder, 
            self.fast_iterations, 
            self.slow_iterations, 
            'NGO'
        )

        print('Running N-Grams')
        builder = lambda i: MapElites(
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
            rng_seed=self.seed + i
        )
        gram_bins, gram_counts, gram_search = self.run_generator(
            runs, 
            builder, 
            0, 
            0, 
            'Gram'
        )

        #######################################################################
        print('Saving results')
        f = open(join(self.data_dir, 'counts.json'), 'w')
        f.write(json_dumps({
            'standard_n': so_counts,
            'ngo': ng_counts,
            'grammar': gram_counts
        }, indent=2))

        #######################################################################
        print('Saving Bins...')
        f = open(join(self.data_dir, 'bins.json'), 'w')
        f.write(json_dumps({
            'runs': runs,
            'resolution': self.resolution,
            'x_label': self.feature_names[0],
            'y_label': self.feature_names[1],
            'methods': {
                'ME-SO': so_bins,
                'ME-NGO': ng_bins,
                'Gram': gram_bins
            }
        }, indent=2))
        f.close()

        #######################################################################
        print('Storing Valid Levels...')
        searches = [so_search.bins, ng_search.bins, gram_search.bins]

        for levels_dir, bins in zip(level_paths, searches):
            for key in bins:
                if bins[key][0][0] == 0.0:
                    with open(join(levels_dir, f'{key[0]}-{key[1]}.txt'), 'w') as f:
                        self.write_level(f, bins[key][0][1])
        
        #######################################################################
        print('Starting Plotters...')
        Popen(['python3', join('Scripts', 'build_counts_graph.py'), self.data_dir, str(self.start_population_size)])
        Popen(['python3', join('Scripts', 'build_counts_grid.py'), self.data_dir])
