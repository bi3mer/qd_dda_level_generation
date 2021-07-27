from Utility import rows_into_columns, Bar, update_progress
from Utility.Math import median, mean, rmse
from Utility.LinkerGeneration import *

from itertools import chain, repeat
from statistics import stdev
from random import seed, choices
from os.path import join
from json import dump, load

class RandomWalkthrough:
    def __init__(self, config, rng_seed):
        self.config = config

        if rng_seed != None:
            seed(rng_seed)

    def __combine(self, segments, algorithm, stop_at_first):
        level = segments[0].copy()
        links = []
        bc_target = {}
        bc_link = {}
        for alg in self.config.feature_names:
            bc_target[alg] = []
            bc_link[alg] = []

        for i in range(1, len(segments)):
            # calculate target behavioral characteristic values
            bc_0 = [alg(segments[i - 1]) for alg in self.config.feature_descriptors]
            bc_1 = [alg(segments[i]) for alg in self.config.feature_descriptors]
            for index, alg in enumerate(self.config.feature_names):
                bc_target[alg].append((bc_0[index] + bc_1[index]) / 2.0)

            # build link 
            link = algorithm(
                self.config.gram, 
                level, 
                segments[i], 
                self.config.get_percent_playable, 
                self.config.feature_descriptors,
                stop_at_first)

            # if the link cannot be formed then return early where True represents
            # that a link could not be built. 
            if link == None:
                return None, None, None, True

            if len(link) == 0:
                # if the length of the link is 0, then there is no error in the target
                # BC and the found BC
                for alg in self.config.feature_names:
                    bc_link[alg].append(bc_target[alg][-1])
            else:
                # otherwise, calculate BC for the link
                for bc, alg in zip(self.config.feature_descriptors, self.config.feature_names):
                    bc_link[alg].append(bc(link))

            links.append(link)
            
            level.extend(link)
            assert self.config.gram.count_bad_n_grams(level) == 0
            level.extend(segments[i].copy())
            assert self.config.gram.count_bad_n_grams(level) == 0

        bc = [rmse(bc_target[alg], bc_link[alg]) for alg in self.config.feature_names]
        return level, links, bc, False

    def build_row(self, name, scores):
        return [
            name,
            round(min(scores), 3),
            round(mean(scores), 3),
            round(median(scores), 3),
            round(max(scores), 3),
            round(max(scores), 3),
            round(stdev(scores), 3)
        ]

    def run(self, runs):
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
        NO_LINK = 'no_link'
        FIRST = 'first'
        BEST = 'best'
        L = 'links'
        BC = 'behavioral_characteristics'
        C  = 'completability'
        CS = 'connection_success'
        CE = 'connection_error'
        S = 'segments'
        R = 'runs'

        stats = {}
        stats['target_size'] = runs
        
        print('WARNING :: stats should have one for each k value!!!!!!!!!!!')
        k_values = [2,3,4]

        for k in k_values:
            print(f'K = {k}')
            progress_bar = Bar(runs * k * 3)
            
            stats[k] = {}
            stats[k][R] = []
            stats[k][BEST] = []
            stats[k][FIRST] = []
            stats[k][NO_LINK] = []

            for _ in range(runs):
                segments = choices(levels, k=k)
                for s in segments:
                    assert self.config.gram.sequence_is_possible(s)
                    assert self.config.get_percent_playable(s) == 1.0

                data = {}
                data[S] = segments

                progress_bar.update(message=f'F')
                level, links, bc, error = self.__combine(segments, exhaustive_link, True)
                if error:
                    progress_bar.update()
                    progress_bar.update()
                    continue
                
                data[FIRST] = {}
                data[FIRST][L] = links
                data[FIRST][BC] = bc
                data[FIRST][C] = self.config.get_percent_playable(level)
                stats[k][FIRST].append(data[FIRST][C] == 1.0)

                progress_bar.update(message=f'A')
                level, links, bc,  error = self.__combine(segments, exhaustive_link, False)

                data[BEST] = {}
                data[BEST][L] = links
                data[BEST][BC] = bc
                data[BEST][C] = self.config.get_percent_playable(level)
                stats[k][BEST].append(data[BEST][C] == 1.0)

                progress_bar.update(message=f'N')
                links = [[] for _ in repeat(None, len(segments))]
                bc = [[0 for __ in repeat(None, len(self.config.feature_names))] for _ in repeat(None, len(segments))]
                level = list(chain(*segments))
                data[NO_LINK] = {}
                data[NO_LINK][L] = links
                data[NO_LINK][BC] = bc
                data[NO_LINK][C] = self.config.get_percent_playable(level)
                stats[k][NO_LINK].append(data[NO_LINK][C] == 1.0)

                stats[k][R].append(data)
            progress_bar.done()


        print('Storing data...')
        f = open(join(self.config.data_dir, 'random_walkthrough_results.json'), 'w')
        dump(stats, f, indent=2)
        f.close()

        

        # print()
        # print('Completability')
        # headers = ['', 'min', 'mean', 'median', 'max', 'std']
        # playability_table = []
        # for k in [NO_LINK, FIRST, BEST]:
        #     row = [k]
        #     scores = []
        #     for s in stats[k]['completability']:
        #         scores.append(s)

        #     row.append(round(min(scores), 3))
        #     row.append(round(mean(scores), 3))
        #     row.append(round(median(scores), 3))
        #     row.append(round(max(scores), 3))
        #     row.append(round(stdev(scores), 3))
        #     playability_table.append(row)
                
        # format_row = "{:>8}" * (len(headers))
        # print(format_row.format(*headers))
        # for _, row in zip(headers, playability_table):
        #     print(format_row.format(*row))

        # print()
        # headers = ['', 'min', 'mean', 'median', 'max', 'std']
        # table = []
        # scores = []

        # # link lengths
        # for links in stats[BEST][L]:
        #     for l in links:
        #         scores.append(len(l))
        # table.append(self.build_row('link size', scores))

        # # behavioral characteristics
        # for index, bc_name in enumerate(self.config.feature_names):
        #     scores = []
        #     for bc_scores in stats[k][BC]:
        #         scores.append(bc_scores[index])
        #     table.append(self.build_row(bc_name, scores))


        # print('Stats')
        # format_row = "{:>9}" * (len(headers))
        # print(format_row.format(*headers))
        # for _, row in zip(headers, table):
        #     print(format_row.format(*row))

        # print()
        # print('Connections')
        # print(f'Successful: {stats[BEST][CS]}')
        # print(f'Error:      {stats[BEST][CE]}')

        # print(f'No Link an be beaten: {sum(no_link_can_be_beaten)} / {levels_to_generate}')
        # print(f'Link an be beaten:    {sum(all_can_be_beaten)} / {levels_to_generate}')
