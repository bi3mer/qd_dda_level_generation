from Utility.GridTools import columns_into_grid_string
from Utility import rows_into_columns, update_progress
from Utility.Math import median, mean
from Utility.LinkerGeneration import *

from itertools import chain, repeat
from random import seed, choices
from os.path import join
from os import listdir
from json import dump

class RandomWalkthrough:
    def __init__(self, config, rng_seed):
        self.config = config

        if rng_seed != None:
            seed(rng_seed)


    def __combine(self, segments, algorithm):
        if algorithm == None:
            return list(chain(*segments)), [0 for _ in repeat(None, len(segments))], [-1 for _ in repeat(None, len(segments))]

        level = segments[0]
        link_lengths = []
        bc = []
        for i in range(1, len(segments)):
            link = algorithm(self.config.gram, level, segments[i], 0)
            
            if len(link) == 0:
                bc.append([-1 for _ in repeat(None, len(segments) - 1)])
            else:
                bc_link = [alg(link) for alg in self.config.feature_descriptors]
                bc_0 = [alg(segments[i - 1]) for alg in self.config.feature_descriptors]
                bc_1 = [alg(segments[i]) for alg in self.config.feature_descriptors]
                bc_mean = [(bc_0[j] + bc_1[j])/2 for j in range(len(bc_0))]
                
                bc.append([abs(bc_link[j] - bc_mean[j]) for j in range(len(bc_mean))])

            link_lengths.append(link)


        return level, link_lengths, bc

    def run(self, levels_to_generate, num_segments):
        print('getting segments')
        levels = []
        level_dir = join(self.config.data_dir, 'levels')
        for level_file_name in listdir(level_dir):
            f = open(join(level_dir, level_file_name))
            if self.config.is_vertical:
                levels.append(rows_into_columns([l.strip() for l in reversed(f.readlines())]))
            else:
                levels.append(rows_into_columns(f.readlines()))

        print('Generating random level combinations')
        stats = {
            'no_link': {
                'lengths': [],
                'behavioral_characteristics': [],
                'completability': []
            },
            'bfs': {
                'lengths': [],
                'behavioral_characteristics': [],
                'completability': []
            },
            'dfs': {
                'lengths': [],
                'behavioral_characteristics': [],
                'completability': []
            },
        }

        link_generator = {
            'no_link': lambda segments: self.__combine(segments, None),
            'bfs': lambda segments: self.__combine(segments, generate_link_bfs),
            'dfs': lambda segments: self.__combine(segments, generate_link_dfs),
        }

        for i in range(levels_to_generate):
            segments = choices(levels, k=num_segments)
            for key in link_generator:
                level, link_lengths, bc = link_generator[key](segments)

                stats[key]['lengths'].append(link_lengths)
                stats[key]['behavioral_characteristics'].append(bc)
                stats[key]['completability'].append(self.config.get_percent_playable(level))

            update_progress(i / levels_to_generate)
        update_progress(1)

        print('Storing data...')
        f = open(join(self.config.data_dir, 'random_walkthrough_results.json'), 'w')
        dump(stats, f, indent=2)
        f.close()

        print('Results')
        # https://www.educba.com/python-print-table/
        # use format() or tabulate()