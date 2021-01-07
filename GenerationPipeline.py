from Utility.GridTools import columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from MapElites import MapElites
from Utility import *

from os.path import isdir, join, exists
from os import mkdir, remove, listdir
from json import dumps as json_dumps
from subprocess import Popen
from random import choice
from csv import writer

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
        print('writing config files for graphing')
        config = {
            'data_file': self.data_file,
            'x_label': self.x_label,
            'y_label': self.y_label,
            'save_file': self.save_file,
            'title': self.title
        }

        f = open(self.map_elites_config, 'w')
        f.write(json_dumps(config))
        f.close()

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
        print('Validating levels. This is somewhat time-consuming but it\'s not horrible...')
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
        Popen(['python', join('Graphing', 'build_map_elites.py'), self.map_elites_config])

        #######################################################################
        print('Building and validating MAP-Elites directed DDA graph. This takes some time...')
        DIRECTIONS = ((0,1), (0,-1), (1, 0), (-1, 0))

        entry_is_valid = {}
        keys = set(search.bins.keys())

        i = 0
        total = len(keys) * 4
        for entry in keys:
            for dir in DIRECTIONS:
                neighbor = (entry[0] + dir[0], entry[1] + dir[1])
                while neighbor not in search.bins:
                    neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                    if not self.__in_bounds(neighbor):
                        break

                if self.__in_bounds(neighbor) and neighbor in search.bins:
                    str_entry_one = str(entry)
                    str_entry_two = str(neighbor)
                    
                    if str_entry_one not in entry_is_valid:
                        entry_is_valid[str_entry_one] = {}
                        entry_is_valid[str_entry_one]['neighbors'] = {}

                    level = generate_link(
                        self.gram, 
                        search.bins[entry][1], 
                        search.bins[neighbor][1], 
                        0)

                    if level == None:
                        entry_is_valid[str_entry_one]['neighbors'][str_entry_two] = -1
                    else:
                        lvl = columns_into_grid_string(level)
                        entry_is_valid[str_entry_one]['neighbors'][str_entry_two] = self.get_percent_playable(lvl)

                i += 1
                update_progress(i/total)
                
        dda_grid_path = join(self.data_dir, 'dda_graph.json')
        f = open(dda_grid_path, 'w')
        f.write(json_dumps(entry_is_valid, indent=2))
        f.close()

        #######################################################################
        print('Starting python process to graph MAP-Elites DDA graph...')
        Popen(['python', join('Graphing', 'build_dda_grid.py'), dda_grid_path, self.data_dir])

        #######################################################################
        print('Running validation on random set of links...')
        iterations = 1000
        percent_completes = {}
        for i in range(iterations):
            path_length = 0
            point = choice(list(search.bins.keys()))
            level = search.bins[point][1].copy()
            path = [point]

            while path_length < self.max_path_length:
                neighbor_keys = list(entry_is_valid[str(point)]['neighbors'].keys())

                if len(neighbor_keys) == 0:
                    break
                
                # get a random neighbor and convert it into a tuple
                point = eval(choice(neighbor_keys))
                level = generate_link(
                    self.gram, 
                    level, 
                    search.bins[point][1], 
                    0)

                path.append(point)
                path_length += 1

            percent_completes[str(path)] = self.get_percent_playable(level)
            update_progress(i/iterations)

        update_progress(1)

        f = open(join(self.data_dir, 'random_walkthroughs.json'), 'w')
        f.write(json_dumps(percent_completes, indent=2))
        f.close()

        mean = sum([percent_completes[key] for key in percent_completes]) / iterations
        print(f'Average Percent Playable: {mean}')
        print('Done!')

    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.resolution

    def get_percent_playable(self, level):
        raise NotImplementedError()