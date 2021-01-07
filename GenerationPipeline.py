from Utility.GridTools import columns_into_grid_string
from MapElites import MapElites
from Utility import *

from csv import writer
from os.path import isdir, join, exists
from os import mkdir, remove, listdir
from json import dumps as json_dumps

class GenerationPipeline():
    def run(self):
        #######################################################################
        print('Setting up data directory...')
        if not isdir(self.data_dir):
            mkdir(self.data_dir)

        level_path = join(self.data_dir, 'levels')
        if not isdir(level_path):
            mkdir(level_path)
        else:
            print('clearing old data...')
            data_file = join(self.data_dir, 'data.csv')

            if exists(data_file):
                remove(data_file)
                
            for filename in listdir(level_path):
                remove(join(level_path, filename))

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
        print('Validating levels (this may take awhile)...')
        f = open(join(self.data_dir, 'data.csv'), 'w')
        w = writer(f)
        w.writerow(self.feature_names + ['performance'])

        num_keys = len(search.bins.keys())
        update_progress(0)
        for i, key in enumerate(search.bins.keys()):
            if self.must_validate:
                is_valid = self.get_percent_playable(search.bins[key][1]) == 1
            else: 
                is_valid = search.bins[key][0] == 1

            w.writerow(list(key) + [search.bins[key][0], is_valid])

            level_file = open(join(level_path, f'{i}.txt'), 'w')
            level_file.write(columns_into_grid_string(search.bins[key][1]))
            level_file.close()

            update_progress(i / num_keys)

        f.close()

        #######################################################################
        print('Starting python process to graph MAP-Elites bins...')

        #######################################################################
        # print('Building and validating MAP-Elites directed DDA graph...')
        # DIRECTIONS = ((0,1), (0,-1), (1, 0), (-1, 0))

        # entry_is_valid = {}
        # keys = set(search.bins.keys())

        # i = 0
        # total = len(keys) * 4
        # for entry in keys:
        #     if
        #     self.test_entry(entry, entry_is_valid)

        #     for dir in DIRECTIONS:
        #         neighbor = (entry[0] + dir[0], entry[1] + dir[1])
        #         while neighbor not in search.bins:
        #             neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
        #             if not self.__in_bounds(neighbor):
        #                 break

        #         if self.__in_bounds(neighbor) and neighbor in search.bins:
        #             self.test_entry(neighbor, entry_is_valid)
        #             self.test_two_entries(entry, neighbor, entry_is_valid)

        #         i += 1
        #         update_progress(i/total)
                
        # f = open(join(self.data_dir, 'dda_graph.json'), 'w')
        # f.write(json_dumps(entry_is_valid, indent=2))
        # f.close()

        # update_progress(1)

        #######################################################################
        print('Starting python process to graph MAP-Elites DDA graph...')

        #######################################################################
        print('Running validation on random set of links...')

    def build_flawed_agents_links(self):
        pass

    def get_percent_playable(self, level):
        raise NotImplementedError()