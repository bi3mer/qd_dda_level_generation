from Utility import rows_into_columns, update_progress
from Utility.Math import median, mean
from Utility.LinkerGeneration import *

from itertools import chain, repeat
from statistics import stdev
from random import seed, choices
from os.path import join
from json import dump, load
from sys import exit

class RandomWalkthrough:
    def __init__(self, config, rng_seed):
        self.config = config

        if rng_seed != None:
            seed(rng_seed)


    def __combine(self, segments, algorithm):
        if algorithm == None:
            links = [[] for _ in repeat(None, len(segments))]
            bc = [[0 for __ in repeat(None, len(self.config.feature_names))] for _ in repeat(None, len(segments))]
            return list(chain(*segments)), links, bc

        level = segments[0]
        links = []
        bc = []
        for i in range(1, len(segments)):
            bc_0 = [alg(segments[i - 1]) for alg in self.config.feature_descriptors]
            bc_1 = [alg(segments[i]) for alg in self.config.feature_descriptors]
            bc_mean = [(bc_0[j] + bc_1[j])/2 for j in range(len(bc_0))]
            # if algorithm == NOne:
                # link = algorithm(self.config.gram, level, segments[i], self.config.feature_descriptors, bc_mean)
            # else:
            link = algorithm(self.config.gram, level, segments[i], 0, agent=self.config.get_percent_playable)
            
            if link == None:
                print(level)
                print(segments[i])
                print(bc_mean)
                exit(-1)

            if len(link) == 0:
                bc.append([0 for _ in repeat(None, len(segments) - 1)])
            else:
                bc_link = [alg(link) for alg in self.config.feature_descriptors]
                bc.append([abs(bc_link[j] - bc_mean[j]) for j in range(len(bc_mean))])

            links.append(link)

            
            level.extend(link)
            assert self.config.gram.count_bad_n_grams(level) == 0
            level.extend(segments[i])
            assert self.config.gram.count_bad_n_grams(level) == 0

        return level, links, bc

    def run(self, levels_to_generate, num_segments):
        print('getting segments')
        level_dir = join(self.config.data_dir, 'levels')
        levels = []
        
        f = open(join(self.config.data_dir, 'generate_corpus_info.json'))
        level_info = load(f)
        f.close()

        for level_name in level_info['fitness']:
            if level_info['fitness'][level_name] == 0.0:
                f = open(join(level_dir, level_name))
                levels.append(rows_into_columns(f.readlines()))
                f.close()

                assert self.config.gram.sequence_is_possible(levels[-1])

        print('Generating random level combinations')
        stats = {
            'no_link': {
                'links': [],
                'behavioral_characteristics': [],
                'completability': []
            },
            'bfs': {
                'links': [],
                'behavioral_characteristics': [],
                'completability': []
            },
            # 'dfs': {
            #     'links': [],
            #     'behavioral_characteristics': [],
            #     'completability': []
            # },
            # 'mcts': {
            #     'links': [],
            #     'behavioral_characteristics': [],
            #     'completability': []
            # },
        }

        link_generator = {
            'no_link': lambda segments: self.__combine(segments, None),
            'bfs': lambda segments: self.__combine(segments, generate_link_bfs),
            # 'dfs': lambda segments: self.__combine(segments, generate_link_dfs),
            # 'mcts': lambda segments: self.__combine(segments, generate_link_mcts),
        }

        update_progress(0)
        for i in range(levels_to_generate):
            segments = choices(levels, k=num_segments)
            for s in segments:
                assert self.config.gram.sequence_is_possible(s)
                assert self.config.get_percent_playable(s) == 1.0

            for key in link_generator:
                level, links, bc = link_generator[key](segments)

                stats[key]['links'].append(links)
                stats[key]['behavioral_characteristics'].append(bc)
                stats[key]['completability'].append(self.config.get_percent_playable(level))
                print(columns_into_grid_string(level))

            update_progress(i / levels_to_generate)
        update_progress(1)


        print('Storing data...')
        f = open(join(self.config.data_dir, 'random_walkthrough_results.json'), 'w')
        dump(stats, f, indent=2)
        f.close()

        print('Link Lengths')
        keys = list(link_generator.keys())
        headers = ['', 'min', 'mean', 'median', 'max', 'std']
        playability_table = []
        for k in keys:
            row = [k]
            scores = []
            for links in stats[k]['links']:
                for l in links:
                    scores.append(len(l))

            row.append(round(min(scores), 3))
            row.append(round(mean(scores), 3))
            row.append(round(median(scores), 3))
            row.append(round(max(scores), 3))
            row.append(round(stdev(scores), 3))
            playability_table.append(row)
                
        format_row = "{:>8}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, playability_table):
            print(format_row.format(*row))

        print()
        print('Completability')
        headers = ['', 'min', 'mean', 'median', 'max', 'std']
        playability_table = []
        for k in keys:
            row = [k]
            scores = []
            for s in stats[k]['completability']:
                scores.append(s)

            row.append(round(min(scores), 3))
            row.append(round(mean(scores), 3))
            row.append(round(median(scores), 3))
            row.append(round(max(scores), 3))
            row.append(round(stdev(scores), 3))
            playability_table.append(row)
                
        format_row = "{:>8}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, playability_table):
            print(format_row.format(*row))

        print()
        print(self.config.feature_names[0])
        headers = ['', 'min', 'mean', 'median', 'max', 'std']
        playability_table = []
        for k in keys:
            row = [k]
            scores = []
            for bc_scores in stats[k]['behavioral_characteristics']:
                for link_score in bc_scores:
                    scores.append(link_score[0])

            row.append(round(min(scores), 3))
            row.append(round(mean(scores), 3))
            row.append(round(median(scores), 3))
            row.append(round(max(scores), 3))
            row.append(round(stdev(scores), 3))
            playability_table.append(row)
                
        format_row = "{:>8}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, playability_table):
            print(format_row.format(*row))

        print()
        print(self.config.feature_names[1])
        headers = ['', 'min', 'mean', 'median', 'max', 'std']
        playability_table = []
        for k in keys:
            row = [k]
            scores = []
            for bc_scores in stats[k]['behavioral_characteristics']:
                for link_score in bc_scores:
                    scores.append(link_score[1])

            row.append(round(min(scores), 3))
            row.append(round(mean(scores), 3))
            row.append(round(median(scores), 3))
            row.append(round(max(scores), 3))
            row.append(round(stdev(scores), 3))
            playability_table.append(row)
                
        format_row = "{:>8}" * (len(headers))
        print(format_row.format(*headers))
        for _, row in zip(headers, playability_table):
            print(format_row.format(*row))
