from os.path import join, exists, isdir
from random import seed

from Utility.LinkerGeneration import *
from Utility import rows_into_columns, update_progress
import json

class GenerateLinks:
    def __init__(self, config, __seed):
        self.config = config
        seed(__seed)

    def __in_bounds(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] <= self.config.resolution and \
               coordinate[1] >= 0 and coordinate[1] <= self.config.resolution

    def run(self):
        #######################################################################
        print('loading bins...')
        level_dir =  join(self.config.data_dir, 'levels')
        if not exists(level_dir) or not isdir(level_dir):
            print(f'{level_dir} is not made. Run --generate-corpus first.')

        bins = {}
        f = open(f'{self.config.data_file}_generate_corpus_data.csv')
        f.readline() # skip header
        for line in f.readlines():
            result = line.strip().split(',')
            performance = float(result[-1])
            if performance != 0.0:
                continue

            key = tuple([int(num) for num in result[:-2]])
            index = int(result[-2])
            if key not in bins:
                bins[key] = []

            level_file = open(join(level_dir, f'{key[1]}_{key[0]}_{index}.txt'), 'r')
            bins[key].append(rows_into_columns(level_file.readlines()))
            level_file.close()

        f.close()

        #######################################################################
        print('Building and validating MAP-Elites directed DDA graph...')
        DIRECTIONS = ((0,0), (0,1), (0,-1), (1, 0), (-1, 0))

        dda_graph = {}
        keys = set(bins.keys())

        i = 0
        link_count = 0

        for k in keys: # iterate through keys
            update_progress(i/len(keys))

            f1_values = [val*(self.config.feature_dimensions[i][1] - self.config.feature_dimensions[i][0])/100 + self.config.feature_dimensions[i][0] for i, val in enumerate(k)]
            for entry_index, entry in enumerate(bins[k]): # iterate through elites
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
                        start = entry
                        for n_index, n_entry in enumerate(bins[neighbor]):
                            # we don't want the possibility for something to connect to itself.config.
                            if dir == (0,0) and n_index == entry_index:
                                continue

                            str_entry_two = f'{neighbor[0]},{neighbor[1]},{n_index}'
                            end = n_entry
                            link_count += 1

                            # this is how I i took the score and put it into the clamped range. 
                            # So I just need to reverse the math and then I'm in business.
                            #
                            # score_in_range = (score - minimum) * 100 / (maximum - minimum) 
                            # feature_vector[i] = floor(score_in_range / self.config.resolution)
                            f2_values = [val*(self.config.feature_dimensions[i][1] - self.config.feature_dimensions[i][0])/100 + self.config.feature_dimensions[i][0] for i, val in enumerate(k)]
                            f_targets = [(f1_values[i] + f2_values[i])/2 for i in range(len(f2_values))]

                            dda_graph[str_entry_one][str_entry_two] = {
                                'targets': f_targets
                            }

                            for KEY in self.config.LINKERS:
                                link = self.config.LINKERS[KEY](start, end)

                                # case for when no link is found
                                if link == None:
                                    dda_graph[str_entry_one][str_entry_two][KEY] = {
                                        'percent_playable': -1,
                                        'link': [],
                                        'behavioral_characteristics': []
                                    }
                                    continue

                                level = start + link + end
                                PERCENT_PLAYABLE = self.config.get_percent_playable(level)
                                if link == []:
                                    # link found is empty which means the behavioral characteristics
                                    # are perfect
                                    dda_graph[str_entry_one][str_entry_two][KEY] = {
                                        'percent_playable': PERCENT_PLAYABLE,
                                        'link': link,
                                        'behavioral_characteristics': [-1 for _ in self.config.feature_descriptors]
                                    }
                                else:
                                    # otherwise, test behavioral characteristics
                                    dda_graph[str_entry_one][str_entry_two][KEY] = {
                                        'percent_playable': PERCENT_PLAYABLE,
                                        'link': link,
                                        'behavioral_characteristics': [bc(link) for bc in self.config.feature_descriptors]
                                    }

            i += 1

        f = open(join(self.config.data_dir, 'dda_graph.json'), 'w')
        f.write(json.dumps(dda_graph, indent=1))
        f.close()