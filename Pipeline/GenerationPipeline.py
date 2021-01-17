from Utility.GridTools import columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from MapElites import MapElites
from Utility import *

from os.path import isdir, join, exists
from os import mkdir, remove, listdir
from json import load as json_load, dumps as json_dumps
from subprocess import Popen
from random import choice
from csv import writer

class GenerationPipeline():
    def run(self):
        output_data = []

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
            
            if exists(join(self.data_dir, 'info.txt')):
                remove(join(self.data_dir, 'info.txt'))

        #######################################################################
        print('writing config files for graphing')
        config = {
            'data_file': self.data_file,
            'x_label': self.x_label,
            'y_label': self.y_label,
            'save_file': self.save_file,
            'title': self.title,
            'resolution': self.resolution
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
        print('Validating levels...')
        valid_levels = 0 
        invalid_levels = 0
        scores = []
        
        f = open(join(self.data_dir, 'data.csv'), 'w')
        w = writer(f)
        w.writerow(self.feature_names + ['performance'])

        num_keys = len(search.bins.keys())
        update_progress(0)
        for i, key in enumerate(search.bins.keys()):
            playability = self.get_percent_playable(search.bins[key][1])
            scores.append(playability)

            if playability == 1.0:
                valid_levels += 1
            else:
                invalid_levels += 1

            w.writerow(list(key) + [self.get_fitness(search.bins[key][1], playability)])

            level_file = open(join(level_path, f'{i}.txt'), 'w')
            level_file.write(columns_into_grid_string(search.bins[key][1]))
            level_file.close()

            update_progress(i / num_keys)

        f.close()

        output_data.append('\nValidation Results:')
        output_data.append(f'Valid Levels: {valid_levels}')
        output_data.append(f'Invalid Levels: {invalid_levels}')
        output_data.append(f'Total Levels: {invalid_levels + valid_levels}')
        output_data.append(f'Mean Scores: {sum(scores) / len(scores)}')

        #######################################################################
        print('Starting python process to graph MAP-Elites bins...')
        Popen(['python', join('Scripts', 'build_map_elites.py'), self.map_elites_config])

        #######################################################################
        if self.skip_after_map_elites:
            self.write_info_file(output_data)
            return

        print('Building and validating MAP-Elites directed DDA graph...')
        DIRECTIONS = ((0,1), (0,-1), (1, 0), (-1, 0))

        entry_is_valid = {}
        keys = set(search.bins.keys())

        i = 0
        total = len(keys) * 4
        playable_scores = []
        link_lengths = []
        link_count = 0

        for entry in keys:
            if search.bins[entry][0] != 0.0:
                entry_is_valid[str(entry)] = {}
                continue

            for dir in DIRECTIONS:
                neighbor = (entry[0] + dir[0], entry[1] + dir[1])
                while neighbor not in search.bins:
                    neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                    if not self.__in_bounds(neighbor):
                        break

                if self.__in_bounds(neighbor) and neighbor in search.bins:
                    link_count += 1
                    str_entry_one = str(entry)
                    str_entry_two = str(neighbor)
                    
                    if str_entry_one not in entry_is_valid:
                        entry_is_valid[str_entry_one] = {}

                    level, length = generate_link(
                        self.gram, 
                        search.bins[entry][1], 
                        search.bins[neighbor][1], 
                        0,
                        include_path_length=True)

                    if level == None:
                        entry_is_valid[str_entry_one][str_entry_two] = -1
                    else:
                        playable = self.get_percent_playable(level)
                        playable_scores.append(playable)
                        entry_is_valid[str_entry_one][str_entry_two] = playable

                        if playable == 1.0:
                            link_lengths.append(length)

                i += 1
                update_progress(i/total)
                
        f = open(join(self.data_dir, 'dda_graph.json'), 'w')
        f.write(json_dumps(entry_is_valid, indent=2))
        f.close()

        output_data.append('\nLink Lengths')
        output_data.append(f'min: {min(link_lengths)}')
        output_data.append(f'mean: {sum(link_lengths) / len(link_lengths)}')
        output_data.append(f'max: {max(link_lengths)}')

        output_data.append('\nLink Counts')
        output_data.append(f'# valid links: {len(link_lengths)}')
        output_data.append(f'# links: {link_count}')

        output_data.append(f'\nLink Playability: {sum(playable_scores) / len(playable_scores)}')

        #######################################################################
        print('Starting python process to graph MAP-Elites DDA graph...')
        Popen(['python', join('Scripts', 'build_dda_grid.py'), self.data_dir])

        #######################################################################
        print('Running validation on random set of links...')
        iterations = 1000
        percent_completes = {}

        valid_levels= 0
        scores = []

        while len(percent_completes) < iterations:
            path_length = 0
            point = eval(choice(list(entry_is_valid.keys())))
            level = search.bins[point][1].copy()
            path = [point]

            while path_length < self.max_path_length:
                neighbors = entry_is_valid[str(point)]
                valid_keys = []

                for key in neighbors.keys():
                    if neighbors[key] == 1.0 and key not in path:
                        valid_keys.append(key)

                if len(valid_keys) == 0:
                    break
                
                # get a random neighbor and convert it into a tuple
                point = eval(choice(valid_keys))
                level = generate_link(
                    self.gram, 
                    level, 
                    search.bins[point][1], 
                    0)

                path.append(point)
                path_length += 1

            if path_length >= 2:
                score = self.get_percent_playable(level)
                scores.append(score)
                percent_completes[str(path)] = score
                update_progress(len(percent_completes) / iterations)

                if score == 1.0:
                    valid_levels += 1
            else:
                print('Unable to find valid level. Trying again.')

        output_data.append('\nWalkthrough Results')
        output_data.append(f'Result: {valid_levels} / {iterations}')
        output_data.append(f'Min Scores: {sum(scores) / len(scores)}')
        output_data.append(f'Mean Scores: {sum(scores) / len(scores)}')
        output_data.append(f'Max Scores: {sum(scores) / len(scores)}')

        f = open(join(self.data_dir, 'random_walkthroughs.json'), 'w')
        f.write(json_dumps(percent_completes, indent=2))
        f.close()

        self.write_info_file(output_data)

    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.resolution

    def run_flawed_agents(self):
        f = open(join(self.data_dir, 'dda_graph.json'), 'r')
        grid = json_load(f)
        f.close()

        f = open(join(self.data_dir, 'data.csv'), 'r')
        f.readline() # get rid of header
        bins = {}
        for i, line in enumerate(f.readlines()):
            linearity, leniency, _ = line.split(',')

            level_file = open(join(self.data_dir, 'levels', f'{i}.txt'))
            bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
            level_file.close()
        f.close()

        for flawed_agent in self.flawed_agents:
            print(f'\nRunning agent: {flawed_agent}')
            result = {}

            for i, src_str in enumerate(grid):
                neighbors = grid[src_str]
                src = eval(src_str)
                new_neighbors = {}

                src_playability = self.get_percent_playable(bins[src], agent=flawed_agent)

                for dst_str in neighbors:
                    if neighbors[dst_str] == 0.0:
                        dst = eval(dst_str)
                        level = generate_link(
                            self.gram, 
                            bins[src], 
                            bins[dst], 
                            0)

                        if level == None:
                            new_neighbors[dst_str] = -1
                        elif src_playability == 0.0:
                            playability = self.get_percent_playable(level, agent=flawed_agent)
                            new_neighbors[dst_str] = playability
                        else:
                            new_neighbors[dst_str] = src_playability * len(bins[src]) / len(level)
                    else:
                        new_neighbors[dst_str] = -1
                
                result[src_str] = new_neighbors
                update_progress(i / len(grid))
                    
            dda_grid_path = join(self.data_dir, f'dda_graph_{flawed_agent}.json')
            f = open(dda_grid_path, 'w')
            f.write(json_dumps(result, indent=2))
            f.close()

    def get_percent_playable(self, level, agent=None):
        raise NotImplementedError()

    def get_fitness(self, level, percent_playable, agent=None):
        raise NotImplementedError()

    def write_info_file(self, output_data):
        file_path = join(self.data_dir, 'info.txt')
        if exists(file_path):
            f = open(file_path, 'a')
        else:
            f = open(file_path, 'w')

        f.write('\n'.join(output_data))
        f.close()