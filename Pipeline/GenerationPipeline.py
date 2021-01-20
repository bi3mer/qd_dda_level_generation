from Utility.GridTools import columns_into_grid_string
from Utility.LinkerGeneration import generate_link
from MapElites import MapElites
from Utility import *

from os.path import join, exists
from json import load as json_load, dumps as json_dumps
from random import random
from subprocess import Popen
from random import choice
from csv import writer

class GenerationPipeline():
    def run(self):
        output_data = []

        #######################################################################
        print('Setting up data directory...')
        level_path_standard = join(self.data_dir, 'levels_standard')
        level_path_genetic = join(self.data_dir, 'levels_genetic')
        level_path_combined = join(self.data_dir, 'levels_combined')

        clear_directory(self.data_dir)
        clear_directory(level_path_standard)
        clear_directory(level_path_genetic)
        clear_directory(level_path_combined)

        #######################################################################
        print('writing config files for graphing')
        self.write_config_file('standard')
        self.write_config_file('genetic')
        self.write_config_file('combined')

        #######################################################################
        print('Running MAP-Elites with n-gram operators...')
        gram_search = MapElites(
            self.start_population_size,
            self.feature_descriptors,
            self.feature_dimensions,
            self.resolution,
            self.fast_fitness,
            self.slow_fitness,
            self.minimize_performance,
            self.population_generator,
            self.n_mutator,
            self.n_crossover,
            rng_seed=self.seed
        )
        gram_search.run(self.fast_iterations, self.slow_iterations)

        print('Running MAP-Elites with standard operators...')
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
            rng_seed=self.seed
        )
        standard_search.run(self.fast_iterations, self.slow_iterations)

        #######################################################################
        print('Validating levels...')
        valid_levels_standard = 0 
        invalid_levels_standard = 0
        scores_standard = []

        valid_levels_genetic = 0 
        invalid_levels_genetic = 0
        scores_genetic = []

        valid_levels_combined = 0 
        invalid_levels_combined = 0

        bins_standard = standard_search.bins
        bins_genetic = gram_search.bins
        bins_combined = {}

        f_standard = open(join(self.data_dir, 'data_standard.csv'), 'w')
        f_genetic = open(join(self.data_dir, 'data_genetic.csv'), 'w')
        f_combined = open(join(self.data_dir, 'data_combined.csv'), 'w')

        w_standard = writer(f_standard)
        w_genetic = writer(f_genetic)
        w_combined = writer(f_combined)

        w_standard.writerow(self.feature_names + ['performance'])
        w_genetic.writerow(self.feature_names + ['performance'])
        w_combined.writerow(self.feature_names + ['performance'])

        searched = 0
        total = self.resolution ** 2
        for x in range(self.resolution):
            for y in range(self.resolution):
                key = (x, y)

                found_standard = False
                found_gram = False

                if key in bins_standard:
                    level_standard = bins_standard[key][1]
                    playability_standard = self.get_percent_playable(level_standard)
                    scores_standard.append(playability_standard)

                    if playability_standard == 1.0:
                        valid_levels_standard += 1
                    else:
                        invalid_levels_standard += 1

                    fitness_standard = self.get_fitness(level_standard, playability_standard)
                    if fitness_standard == 0.0:
                        found_standard = True

                    w_standard.writerow(list(key) + [fitness_standard])

                    level_file = open(join(level_path_standard, f'{x}_{y}.txt'), 'w')
                    level_file.write(columns_into_grid_string(level_standard))
                    level_file.close()
                
                if key in bins_genetic:
                    level_genetic = bins_genetic[key][1]
                    playability_genetic = self.get_percent_playable(level_genetic)
                    scores_genetic.append(playability_genetic)

                    if playability_genetic == 1.0:
                        valid_levels_genetic += 1
                    else:
                        invalid_levels_genetic += 1

                    fitness_genetic = self.get_fitness(level_genetic, playability_genetic)
                    if fitness_genetic == 0.0:
                        found_gram = True

                    w_genetic.writerow(list(key) + [fitness_genetic])
                    level_file = open(join(level_path_genetic, f'{x}_{y}.txt'), 'w')
                    level_file.write(columns_into_grid_string(level_genetic))
                    level_file.close()

                level_combined = None
                fitness_combined = None
                if found_gram and found_standard:
                    if random() >= 0.5:
                        level_combined = level_standard
                        fitness_combined = fitness_standard
                        playability_combined = playability_standard
                    else:
                        level_combined = level_genetic
                        fitness_combined = fitness_genetic
                        playability_combined = playability_genetic
                elif found_gram:
                    level_combined = level_genetic
                    fitness_combined = fitness_genetic
                    playability_combined = playability_genetic
                elif found_standard:
                    level_combined = level_standard
                    fitness_combined = fitness_standard
                    playability_combined = playability_standard

                if level_combined != None:
                    valid_levels_combined += 1
                    bins_combined[key] = (playability_combined, level_combined)

                    w_combined.writerow(list(key) + [fitness_combined])
                    level_file = open(join(level_path_combined, f'{x}_{y}.txt'), 'w')
                    level_file.write(columns_into_grid_string(level_combined))
                    level_file.close()

                searched += 1
                update_progress(searched / total)

        f_standard.close()
        f_genetic.close()
        f_combined.close()

        output_data.append('\nValidation Results Standard:')
        output_data.append(f'Valid Levels: {valid_levels_standard}')
        output_data.append(f'Invalid Levels: {invalid_levels_standard}')
        output_data.append(f'Total Levels: {invalid_levels_standard + valid_levels_standard}')
        output_data.append(f'Mean Scores: {sum(scores_standard) / len(scores_standard)}')

        output_data.append('\nValidation Results Genetic:')
        output_data.append(f'Valid Levels: {valid_levels_genetic}')
        output_data.append(f'Invalid Levels: {invalid_levels_genetic}')
        output_data.append(f'Total Levels: {invalid_levels_genetic + valid_levels_genetic}')
        output_data.append(f'Mean Scores: {sum(scores_genetic) / len(scores_genetic)}')

        output_data.append('\nValidation Results Combined:')
        output_data.append(f'Total Levels: {invalid_levels_combined + valid_levels_combined}')

        #######################################################################
        print('Starting python process to graph MAP-Elites bins...')
        Popen(['python', join('Scripts', 'build_map_elites.py'), f'{self.map_elites_config}_standard.json'])
        Popen(['python', join('Scripts', 'build_map_elites.py'), f'{self.map_elites_config}_genetic.json'])
        Popen(['python', join('Scripts', 'build_map_elites.py'), f'{self.map_elites_config}_combined.json'])

        #######################################################################
        if self.skip_after_map_elites:
            self.write_info_file(output_data)
            return

        print('Building and validating MAP-Elites directed DDA graph...')
        DIRECTIONS = ((0,1), (0,-1), (1, 0), (-1, 0))

        entry_is_valid = {}
        keys = set(bins_combined.keys())

        i = 0
        total = len(keys) * 4
        playable_scores = []
        link_lengths = []
        link_count = 0

        for entry in keys:
            if bins_combined[entry][0] != 1.0:
                entry_is_valid[str(entry)] = {}
                continue

            for dir in DIRECTIONS:
                neighbor = (entry[0] + dir[0], entry[1] + dir[1])
                while neighbor not in bins_combined:
                    neighbor = (neighbor[0] + dir[0], neighbor[1] + dir[1])
                    if not self.__in_bounds(neighbor):
                        break

                if self.__in_bounds(neighbor) and neighbor in bins_combined:
                    link_count += 1
                    str_entry_one = str(entry)
                    str_entry_two = str(neighbor)
                    
                    if str_entry_one not in entry_is_valid:
                        entry_is_valid[str_entry_one] = {}

                    level, length = generate_link(
                        self.gram, 
                        bins_combined[entry][1], 
                        bins_combined[neighbor][1], 
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
            level = bins_combined[point][1].copy()
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
                    bins_combined[point][1], 
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
        output_data.append(f'Min Scores: {min(scores)}')
        output_data.append(f'Mean Scores: {sum(scores) / len(scores)}')
        output_data.append(f'Max Scores: {max(scores)}')

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
                        level = generate_link(
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

            Popen(['python', join('Scripts', 'build_dda_grid.py'), self.data_dir, flawed_agent])

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
            'resolution': self.resolution
        }

        f = open(f'{self.map_elites_config}_{operator_type}.json', 'w')
        f.write(json_dumps(config))
        f.close()