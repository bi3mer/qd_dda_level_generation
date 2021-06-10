from Utility.Log import Log
from Utility.GridTools import columns_into_grid_string
from Utility.LinkerGeneration import generate_link_bfs, generate_link_mcts
from MapElites import MapElites
from Utility.Math import *
from Utility import *

from json import load as json_load, dumps as json_dumps
from os.path import join, exists
from subprocess import Popen
from random import choice
from csv import writer

class GenerationPipeline():
    def __init__(self, config, only_map_elites):
        self.config = config
        self.only_map_elites = only_map_elites



    def run(self):
        #######################################################################
        level_dir =  join(self.config.data_dir, 'levels')

        clear_directory(self.config.data_dir)
        clear_directory(level_dir)

        #######################################################################
        print('writing config file for graphing')

        config = {
            'data_file': f'{self.config.data_file}.csv',
            'x_label': self.config.x_label,
            'y_label': self.config.y_label,
            'save_file': f'{self.config.save_file}.pdf',
            'title': self.config.title,
            'resolution': self.config.resolution,
            'feature_dimensions': self.config.feature_dimensions
        }

        f = open(f'{self.config.map_elites_config}.json', 'w')
        f.write(json_dumps(config, indent=2))
        f.close()

        #######################################################################
        print('Running Gram-Elites...')
        gram_search = MapElites(
            self.config.start_population_size,
            self.config.feature_descriptors,
            self.config.feature_dimensions,
            self.config.resolution,
            self.config.fitness,
            self.config.minimize_performance,
            self.config.n_population_generator,
            self.config.n_mutator,
            self.config.n_crossover,
            self.config.elites_per_bin,
            rng_seed=self.config.seed
        )
        gram_search.run(self.config.iterations)

        #######################################################################
        print('Validating levels...')
        valid_levels = 0
        invalid_levels =  0
        fitnesses = []
        bins = gram_search.bins
        f = open(join(self.config.data_dir, 'data.csv'), 'w')
        csv_writer = writer(f)
        csv_writer.writerow(self.config.feature_names + ['performance'])
        
        searched = 0
        total = self.config.resolution ** 2
        for x in range(self.config.resolution):
            for y in range(self.config.resolution): 
                key = (x, y)
                found = []
                if key in bins:
                    for level_index, info in enumerate(bins[key]): # for each elite in the bin
                        # Mario uses a separate simulation but the others do not. 
                        # The simulation does not have to be re-run.
                        level = info[1]

                        if self.config.uses_separate_simulation:
                            playability = self.config.get_percent_playable(level)
                            fitness = self.config.get_fitness(level, playability)
                        else: 
                            fitness = info[0]

                        fitnesses.append(fitness)

                        if fitness == 0.0:
                            found.append((level, fitness, fitness))
                            valid_levels += 1
                        else:
                            invalid_levels += 1

                        csv_writer.writerow(list(key) + [fitness])

                        level_file = open(join(level_dir, f'{x}_{y}_{level_index}.txt'), 'w')
                        level_file.write(columns_into_grid_string(level))
                        level_file.close()

                searched += 1
                update_progress(searched / total)

        f.close()
        results = {
            'valid_levels': valid_levels,
            'invalid_levels': invalid_levels,
            'total_levels': valid_levels + invalid_levels,
            'fitness': fitness,
            'mean_fitness': sum(fitnesses) / len(fitnesses)
        }

        #######################################################################
        if self.only_map_elites:
            self.write_info_file(results)
            Popen(['python3', join('Scripts', 'build_map_elites.py'), self.config.data_dir])
            Popen(['python3', join('Scripts', 'build_combined_map_elites.py'), self.config.data_dir])
            return

        #######################################################################
        print('Building and validating MAP-Elites directed DDA graph...')
        DIRECTIONS = ((0,0), (0,1), (0,-1), (1, 0), (-1, 0))
        KEYS = ['bfs', 'mcts']

        dda_graph = {}
        bins = gram_search.bins
        keys = set(bins.keys())


        i = 0
        link_count = 0

        print('WARNING: this will not work Mario right now if a simulation is used.')
        successes = 0
        failures  = 0
        for k in keys: # iterate through keys
            if key == (6,16):
                print('a')

            f1_values = [val*(self.config.feature_dimensions[i][1] - self.config.feature_dimensions[i][0])/100 + self.config.feature_dimensions[i][0] for i, val in enumerate(k)]
            for entry_index, entry in enumerate(bins[k]): # iterate through elites
                if entry[0] != 0.0:
                    continue
                
                str_entry_one = f'{k[0]},{k[1]},{entry_index}'
                if str_entry_one not in dda_graph:
                    dda_graph[str_entry_one] = {}

                for dir in DIRECTIONS:
                    neighbor = (k[0] + dir[0], k[1] + dir[1])
                    while neighbor not in bins:
                        neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                        
                        if not self.__in_bounds(neighbor):
                            break

                    if neighbor in bins:
                        start = entry[1]
                        for n_index, n_entry in enumerate(bins[neighbor]):
                            # we don't want the possibility for something to connect to itself.config.
                            if dir == (0,0) and n_index == entry_index:
                                continue

                            if n_entry[0] != 0.0:
                                continue
                            
                            str_entry_two = f'{neighbor[0]},{neighbor[1]},{n_index}'
                            end = n_entry[1]
                            link_count += 1

                            # this is how I i took the score and put it into the clamped range. 
                            # So I just need to reverse the math and then I'm in business.
                            #
                            # score_in_range = (score - minimum) * 100 / (maximum - minimum) 
                            # feature_vector[i] = floor(score_in_range / self.config.resolution)
                            f2_values = [val*(self.config.feature_dimensions[i][1] - self.config.feature_dimensions[i][0])/100 + self.config.feature_dimensions[i][0] for i, val in enumerate(k)]
                            f_targets = [(f1_values[i] + f2_values[i])/2 for i in range(len(f2_values))]

                            # TODO: log length, behavioral characteristics, and targets
                            dda_graph[str_entry_one][str_entry_two] = {
                                'targets': f_targets
                            }

                            bfs_link = generate_link_bfs(self.config.gram, start, end, 0)
                            mcts_link = generate_link_mcts(self.config.gram, start, end, self.config.feature_descriptors, f_targets)
                            if mcts_link == None:
                                failures += 1
                            else:
                                successes += 1

                            for key, link in zip(KEYS, [bfs_link, mcts_link]):
                                if link == None:
                                    dda_graph[str_entry_one][str_entry_two][key] = {
                                        'percent_playable': -1,
                                        'link': [],
                                        'behavioral_characteristics': []
                                    }
                                elif link == []:
                                    level = start + link + end
                                    dda_graph[str_entry_one][str_entry_two][key] = {
                                        'percent_playable': self.config.get_percent_playable(level),
                                        'link': link,
                                        'behavioral_characteristics': [-1 for _ in self.config.feature_descriptors]
                                    }
                                else:
                                    level = start + link + end
                                    dda_graph[str_entry_one][str_entry_two][key] = {
                                        'percent_playable': self.config.get_percent_playable(level),
                                        'link': link,
                                        'behavioral_characteristics': [bc(link) for bc in self.config.feature_descriptors]
                                    }

            i += 1
            update_progress(i/len(keys))
                
        print(f'Link Connections Found: {successes} / {successes + failures}')
        f = open(join(self.config.data_dir, 'dda_graph.json'), 'w')
        f.write(json_dumps(dda_graph, indent=1))
        f.close()

        results['possible_links'] = link_count
        results['mcts'] = {
            'success': successes,
            'failure': failures
        }

        #######################################################################
        print('Running validation on random set of links...')
        iterations = 1000
        self.__run_walkthrough(bins, dda_graph, KEYS[0], False, results, iterations)
        self.__run_walkthrough(bins, dda_graph, KEYS[1], False, results, iterations)
        # self.__run_walkthrough(bins, dda_graph, KEYS[1], True, results, iterations)

        f = open(join(self.config.data_dir, 'results.json'), 'w')
        f.write(json_dumps(results, indent=2))
        f.close()

        #######################################################################
        print('Starting python graphing processes...\n\n')
        Popen(['python3', join('Scripts', 'build_map_elites.py'), self.config.data_dir])
        Popen(['python3', join('Scripts', 'build_dda_grid.py'), self.config.data_dir])


    
    def __run_walkthrough(self, bins, dda_graph, algorithm_key, use_repair, results, iterations):
        percent_completes = {}

        duplicates_found = 0
        valid_levels = 0
        levels= []
        scores = []
        modifications = []
        characteristics_of_segments = []
        characteristics_with_links = []
        characteristics_with_repair = []

        while len(percent_completes) < iterations:
            path_length = 0
            next_choice = choice(list(dda_graph.keys()))
            start_split = next_choice.split(',')
            point = (int(start_split[0]), int(start_split[1]))
            level = bins[point][int(start_split[2])][1]
            path = [point]
            segment_characteristics = [0 for _ in range(len(self.config.feature_descriptors))]
            previous_choice = None

            while path_length < self.config.max_path_length:
                previous_choice = next_choice
                neighbors = dda_graph[previous_choice]
                valid_neighbors = []

                for key in neighbors.keys():
                    if key not in path and neighbors[key][algorithm_key]['percent_playable'] == 1.0: 
                        valid_neighbors.append(key)

                if len(valid_neighbors) == 0:
                    break

                next_choice = choice(list(dda_graph[previous_choice].keys()))
                start_split = next_choice.split(',')
                point = (int(start_split[0]), int(start_split[1]))
                end = bins[point][int(start_split[2])][1]

                segment = dda_graph[previous_choice][next_choice][algorithm_key]['link']
                segment_characteristics = [segment_characteristics[i] + fd(level) for i, fd in enumerate(self.config.feature_descriptors)]
                level = level + segment + end

                path.append(next_choice)
                path_length += 1

            str_path = str(path)
            if str_path in percent_completes:
                duplicates_found += 1
                if duplicates_found > 1000:
                    print('WARNING: Found over 1000 duplicates.')
                    break
            elif path_length > 2:
                characteristics_with_links.append([fd(level) for fd in self.config.feature_descriptors])
                
                if use_repair:
                    level, modifications_made = self.config.repair_level(level)
                    characteristics_with_repair.append([fd(level) for fd in self.config.feature_descriptors])
                else:
                    modifications_made = 0
                    characteristics_with_repair.append([])

                score = self.config.get_percent_playable(level)
                percent_completes[str_path] = score
                scores.append(score)
                levels.append(level)
                characteristics_of_segments.append([c_score / path_length for c_score in segment_characteristics])
                modifications.append(modifications_made)

                update_progress(len(levels) / iterations)

                if score == 1.0:
                    valid_levels += 1
            else:
                print(f'WARNING: Unable to find valid level for {algorithm_key}_{use_repair}. Trying again. ')

        output = {}
        output['levels'] = levels
        output['valid_levels'] = valid_levels
        output['scores'] = scores
        output['duplicates_found'] = duplicates_found
        output['modifications'] = modifications
        output['characteristics_of_segments'] = characteristics_of_segments
        output['characteristics_with_links'] = characteristics_with_links
        output['characteristics_with_repair'] = characteristics_with_repair

        if 'walkthrough' not in results:
            results['walkthrough'] = {}

        results['walkthrough'][f'{algorithm_key}_{use_repair}'] = output



    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.config.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.config.resolution



    def run_flawed_agents(self):
        f = open(join(self.config.data_dir, 'dda_graph.json'), 'r')
        grid = json_load(f)
        f.close()

        f = open(join(self.config.data_dir, 'data_combined.csv'), 'r')
        f.readline() # get rid of header
        bins = {}
        for line in f.readlines():
            linearity, leniency, _ = line.split(',')

            level_file = open(join(self.config.data_dir, 'levels_combined', f'{linearity}_{leniency}.txt'))
            bins[(int(linearity), int(leniency))] = rows_into_columns(level_file.readlines())
            level_file.close()
        f.close()

        for flawed_agent in self.config.flawed_agents:
            print(f'\nRunning agent: {flawed_agent}')
            result = {}

            for i, src_str in enumerate(grid):
                neighbors = grid[src_str]
                src = eval(src_str)
                new_neighbors = {}

                src_playability = self.config.get_percent_playable(bins[src], agent=flawed_agent)

                for dst_str in neighbors:
                    if neighbors[dst_str] == 1.0:
                        dst = eval(dst_str)
                        level = generate_link_bfs(
                            self.config.gram, 
                            bins[src], 
                            bins[dst], 
                            0)

                        if level == None:
                            new_neighbors[dst_str] = -1
                        elif src_playability == 1.0:
                            playability = self.config.get_percent_playable(level, agent=flawed_agent)
                            new_neighbors[dst_str] = playability
                        else:
                            new_neighbors[dst_str] = src_playability * len(bins[src]) / len(level)
                    else:
                        new_neighbors[dst_str] = -1
                
                result[src_str] = new_neighbors
                update_progress(i / len(grid))
                    
            dda_grid_path = join(self.config.data_dir, f'dda_graph_{flawed_agent}.json')
            f = open(dda_grid_path, 'w')
            f.write(json_dumps(result, indent=2))
            f.close()

            Popen(['python3', join('Scripts', 'build_dda_grid.py'), self.config.data_dir, flawed_agent])



    def write_info_file(self, output_data):
        file_path = join(self.config.data_dir, 'info.txt')
        if exists(file_path):
            f = open(file_path, 'a')
        else:
            f = open(file_path, 'w')

        f.write(json_dumps(output_data, indent=2))
        f.close()
