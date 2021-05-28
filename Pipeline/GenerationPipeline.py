from Utility.Log import Log
from Utility.GridTools import columns_into_grid_string
from Utility.LinkerGeneration import generate_link_bfs, generate_link_mcts
from MapElites import MapElites
from Utility import *

from json import load as json_load, dumps as json_dumps
from os.path import join, exists
from subprocess import Popen
from itertools import repeat
from random import choice
from csv import writer

class GenerationPipeline():
    def run(self):
        output_data = []

        #######################################################################
        level_paths = [
            join(self.data_dir, 'levels_standard'),
            join(self.data_dir, 'levels_standard_n'),
            join(self.data_dir, 'levels_genetic'),
        ]

        clear_directory(self.data_dir)
        for path in level_paths:
            clear_directory(path)

        log = Log.Log(0, self.data_dir)

        #######################################################################
        log.log_info('writing config files for graphing')
        self.write_config_file('standard')
        self.write_config_file('standard_n')
        self.write_config_file('genetic')

        #######################################################################
        log.log_info('Running MAP-Elites with standard operators...')
        standard_search = MapElites(
            self.start_population_size,
            self.feature_descriptors,
            self.feature_dimensions,
            self.resolution,
            self.fitness,
            self.minimize_performance,
            self.population_generator,
            self.mutator,
            self.crossover,
            self.elites_per_bin,
            rng_seed=self.seed
        )
        print('WARNING: not running standard search')
        standard_search.run(0)

        log.log_info('Running MAP-Elites with standard operators and n-gram population...')
        standard_n_search = MapElites(
            self.start_population_size,
            self.feature_descriptors,
            self.feature_dimensions,
            self.resolution,
            self.fitness,
            self.minimize_performance,
            self.n_population_generator,
            self.mutator,
            self.crossover,
            self.elites_per_bin,
            rng_seed=self.seed
        )
        print('WARNING: not running standard+n search')
        standard_n_search.run(0)

        log.log_info('Running MAP-Elites with n-gram operators...')
        gram_search = MapElites(
            self.start_population_size,
            self.feature_descriptors,
            self.feature_dimensions,
            self.resolution,
            self.fitness,
            self.minimize_performance,
            self.n_population_generator,
            self.n_mutator,
            self.n_crossover,
            self.elites_per_bin,
            rng_seed=self.seed
        )
        gram_search.run(self.iterations)

        #######################################################################
        log.log_info('Validating levels...')
        STANDARD_INDEX = 0
        STANDARD_N_INDEX = 1
        GENETIC_INDEX = 2

        titles = [
            'standard operators', 
            'standard operators + n-gram pop', 
            'n-gram operators', 
        ]

        valid_levels = [0 for _ in repeat(None, 3)]
        invalid_levels =  [0 for _ in repeat(None, 3)]
        fitnesses = [[] for _ in repeat(None, 3)]
        bins = [standard_search.bins, standard_n_search.bins, gram_search.bins]
        files = [
            open(join(self.data_dir, 'data_standard.csv'), 'w'),
            open(join(self.data_dir, 'data_standard_n.csv'), 'w'),
            open(join(self.data_dir, 'data_genetic.csv'), 'w'),
        ]
        
        writers = []
        for f in files:
            w = writer(f)
            w.writerow(self.feature_names + ['performance'])
            writers.append(w)
        
        searched = 0
        total = self.resolution ** 2
        for x in range(self.resolution):
            for y in range(self.resolution): 
                key = (x, y)
                found = []

                for i, bin in enumerate(bins): # for each algorithm type
                    if key in bin:
                        for level_index, info in enumerate(bin[key]): # for each elite in the bin
                            # Mario uses a separate simulation but the others do not. 
                            # The simulation does not have to be re-run.
                            level = info[1]

                            if self.uses_separate_simulation:
                                playability = self.get_percent_playable(level)
                                fitness = self.get_fitness(level, playability)
                            else: 
                                fitness = info[0]

                            fitnesses[i].append(fitness)

                            if fitness == 0.0:
                                found.append((level, fitness, fitness))
                                valid_levels[i] += 1
                            else:
                                invalid_levels[i] += 1

                            writers[i].writerow(list(key) + [fitness])

                            level_file = open(join(level_paths[i], f'{x}_{y}_{level_index}.txt'), 'w')
                            level_file.write(columns_into_grid_string(level))
                            level_file.close()

                searched += 1
                update_progress(searched / total)

        map(lambda f: f.close(), files)
        for i in range(len(titles)):
            output_data.append(f'\nValidation Results {titles[i]}:')
            output_data.append(f'Valid Levels: {valid_levels[i]}')
            output_data.append(f'Invalid Levels: {invalid_levels[i]}')
            output_data.append(f'Total Levels: {invalid_levels[i] + valid_levels[i]}')
            output_data.append(f'Mean Fitness: {sum(fitnesses[i]) / len(fitnesses[i])}')


        #######################################################################
        if self.skip_after_map_elites:
            self.write_info_file(output_data)
            Popen(['python3', join('Scripts', 'build_map_elites.py'), self.data_dir])
            Popen(['python3', join('Scripts', 'build_combined_map_elites.py'), self.data_dir])
            return

        log.log_info('Building and validating MAP-Elites directed DDA graph...')
        DIRECTIONS = ((0,0), (0,1), (0,-1), (1, 0), (-1, 0))

        dda_graph = {}
        bins = gram_search.bins
        keys = set(bins.keys())

        i = 0
        playable_scores = []
        link_lengths = []
        link_count = 0

        print('WARNING: this will not work Mario right now if a simulation is used.')
        successes = 0
        failures  = 0
        for k in keys: # iterate through keys
            f1_values = [val*(self.feature_dimensions[i][1] - self.feature_dimensions[i][0])/100 + self.feature_dimensions[i][0] for i, val in enumerate(k)]
            for entry_index, entry in enumerate(bins[k]): # iterate through elites
                if entry[0] != 0.0:
                    dda_graph[str(entry)] = {}
                    continue

                for dir in DIRECTIONS:
                    neighbor = (k[0] + dir[0], k[1] + dir[1])
                    while neighbor not in bins:
                        neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                        if not self.__in_bounds(neighbor):
                            break

                    if self.__in_bounds(neighbor) and neighbor in bins:
                        str_entry_one = f'{k[0]},{k[1]},{entry_index}'
                        
                        if str_entry_one not in dda_graph:
                            dda_graph[str_entry_one] = {}
                        
                        start = entry[1]
                        for n_index, n_entry in enumerate(bins[neighbor]):
                            # we don't want the possibility for something to connect to itself.
                            if dir == (0,0) and n_index == entry_index:
                                break
                            
                            str_entry_two = f'{neighbor[0]},{neighbor[1]},{n_index}'
                            end = n_entry[1]
                            link_count += 1

                            # this is how I i took the score and put it into the clamped range. 
                            # So I just need to reverse the math and then I'm in business.
                            #
                            # score_in_range = (score - minimum) * 100 / (maximum - minimum) 
                            # feature_vector[i] = floor(score_in_range / self.resolution)
                            f2_values = [val*(self.feature_dimensions[i][1] - self.feature_dimensions[i][0])/100 + self.feature_dimensions[i][0] for i, val in enumerate(k)]
                            f_targets = [(f1_values[i] + f2_values[i])/2 for i in range(len(f2_values))]

                            link = generate_link_mcts(self.gram, start, end, self.feature_descriptors, f_targets)
                            if link == None:
                                link = generate_link_bfs(self.gram, start, end, 0)
                                failures += 1
                            else:
                                successes += 1

                            level = start + link + end

                            if level == None:
                                dda_graph[str_entry_one][str_entry_two] = {
                                    'percent_playable': -1,
                                    'link': link
                                }
                            else:
                                playable = self.get_percent_playable(level)
                                playable_scores.append(playable)
                                dda_graph[str_entry_one][str_entry_two] = {
                                    'percent_playable': playable,
                                    'link': link
                                }

                                if playable == 1.0:
                                    link_lengths.append(len(link))

            i += 1
            update_progress(i/len(keys))
                
        log.log_info(f'Link Connections Found: {successes} / {successes + failures}')
        f = open(join(self.data_dir, 'dda_graph.json'), 'w')
        f.write(json_dumps(dda_graph, indent=1))
        f.close()

        # https://www.geeksforgeeks.org/finding-mean-median-mode-in-python-without-libraries/
        link_lengths.sort()
        if len(link_lengths) % 2 == 0:
            median1 = link_lengths[len(link_lengths)//2] 
            median2 = link_lengths[len(link_lengths)//2 - 1] 
            median = (median1 + median2)/2
        else:
            median = link_lengths[len(link_lengths)//2] 

        output_data.append('\nLink Lengths')
        output_data.append(f'min: {min(link_lengths)}')
        output_data.append(f'mean: {sum(link_lengths) / len(link_lengths)}')
        output_data.append(f'max: {max(link_lengths)}')
        output_data.append(f'median: {median}')
        output_data.append(json_dumps(link_lengths))

        output_data.append('\nLink Counts')
        output_data.append(f'# valid links: {len(link_lengths)}')
        output_data.append(f'# links: {link_count}')

        output_data.append(f'\nLink Playability: {sum(playable_scores) / len(playable_scores)}')

        #######################################################################
        log.log_info('Running validation on random set of links...')
        iterations = 1000
        percent_completes = {}

        duplicates_found = 0
        valid_levels= 0
        scores = []

        while len(percent_completes) < iterations:
            path_length = 0
            next_choice = choice(list(dda_graph.keys()))
            start_split = next_choice.split(',')
            point = (int(start_split[0]), int(start_split[1]))
            level = bins[point][int(start_split[2])][1]
            path = [point]

            while path_length < self.max_path_length:
                previous_choice = next_choice
                neighbors = dda_graph[previous_choice]
                valid_neighbors = []

                for key in neighbors.keys():
                    if neighbors[key]['percent_playable'] == 1.0 and key not in path:
                        valid_neighbors.append(key)

                if len(valid_neighbors) == 0:
                    break

                next_choice = choice(list(dda_graph[previous_choice].keys()))
                start_split = next_choice.split(',')
                point = (int(start_split[0]), int(start_split[1]))
                end = bins[point][int(start_split[2])][1]

                level = level + dda_graph[previous_choice][next_choice]['link'] + end

                path.append(next_choice)
                path_length += 1

            str_path = str(path)
            if str_path in percent_completes:
                duplicates_found += 1
                if duplicates_found > 1000:
                    log.log_warning('Found over 1000 duplicates.')
                    break
            elif path_length > 2:
                score = self.get_percent_playable(level)
                scores.append(score)
                percent_completes[str_path] = score
                update_progress(len(percent_completes) / iterations)

                if score == 1.0:
                    valid_levels += 1
            else:
                log.log_warning('Unable to find valid level. Trying again.')

        output_data.append('\nWalkthrough Results')
        output_data.append(f'Result: {valid_levels} / {iterations}')
        output_data.append(f'Min Scores: {min(scores)}')
        output_data.append(f'Mean Scores: {sum(scores) / len(scores)}')
        output_data.append(f'Max Scores: {max(scores)}')
        output_data.append(f'Duplicates: {duplicates_found}')

        f = open(join(self.data_dir, 'random_walkthroughs.json'), 'w')
        f.write(json_dumps(percent_completes, indent=2))
        f.close()

        self.write_info_file(output_data)

        #######################################################################
        log.log_info('Starting python graphing processes...\n\n')
        Popen(['python3', join('Scripts', 'build_map_elites.py'), self.data_dir])
        Popen(['python3', join('Scripts', 'build_combined_map_elites.py'), self.data_dir])
        Popen(['python3', join('Scripts', 'build_dda_grid.py'), self.data_dir])

    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.resolution

    def run_flawed_agents(self):
        f = open(join(self.data_dir, 'dda_graph.json'), 'r')
        grid = json_load(f)
        f.close()

        f = open(join(self.data_dir, 'data_combined.csv'), 'r')
        f.readline() # get rid of header
        bins = {}
        for line in f.readlines():
            linearity, leniency, _ = line.split(',')

            level_file = open(join(self.data_dir, 'levels_combined', f'{linearity}_{leniency}.txt'))
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
                    if neighbors[dst_str] == 1.0:
                        dst = eval(dst_str)
                        level = generate_link_bfs(
                            self.gram, 
                            bins[src], 
                            bins[dst], 
                            0)

                        if level == None:
                            new_neighbors[dst_str] = -1
                        elif src_playability == 1.0:
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

            Popen(['python3', join('Scripts', 'build_dda_grid.py'), self.data_dir, flawed_agent])

    def get_percent_playable(self, level, agent=None):
        pass # I'd use a not implemented error but pylance makes the code unreachable, sooo.....

    def get_fitness(self, level, percent_playable, agent=None):
        pass  # I'd use a not implemented error but pylance makes the code unreachable, sooo.....

    def write_info_file(self, output_data):
        file_path = join(self.data_dir, 'info.txt')
        if exists(file_path):
            f = open(file_path, 'a')
        else:
            f = open(file_path, 'w')

        f.write('\n'.join(output_data))
        f.close()

    def write_config_file(self, operator_type):
        config = {
            'data_file': f'{self.data_file}_{operator_type}.csv',
            'x_label': self.x_label,
            'y_label': self.y_label,
            'save_file': f'{self.save_file}_{operator_type}.pdf',
            'title': self.title,
            'resolution': self.resolution,
            'feature_dimensions': self.feature_dimensions
        }

        f = open(f'{self.map_elites_config}_{operator_type}.json', 'w')
        f.write(json_dumps(config))
        f.close()