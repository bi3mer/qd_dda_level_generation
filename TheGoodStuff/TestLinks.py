from os.path import join, exists, isdir
from random import seed
from Utility.GridTools import columns_into_grid_string

from Utility.LinkerGeneration import *
from Utility import rows_into_columns, update_progress
import json

class TestLinks:
    def __init__(self, config, __seed):
        self.config = config
        seed(__seed)

    def __string_to_key_and_index(self, string):
        split = string.split(',')
        return tuple([int(val) for val in split[:-1]]), int(split[-1])

    def run(self):
        #######################################################################
        print('Loading bins...')
        level_dir =  join(self.config.data_dir, 'levels')
        if not exists(level_dir) or not isdir(level_dir):
            print(f'{level_dir} is not made. Run --generate-corpus first.')

        bins = {}
        with open(join(self.config.data_dir, 'generate_corpus_info.json')) as f:
            data = json.load(f)
            for file_name in data['fitness']:
                if data['fitness'][file_name] == 0.0:
                    # remove the .txt extension and take all indices except the last one
                    indices = [int(num) for num in file_name[:-4].split('_')]
                    key = tuple(indices[:-1])

                    if key not in bins:
                        bins[key] = [None for _ in range(self.config.elites_per_bin)]
                    
                    with open(join(level_dir, file_name), 'r') as level_file:
                        bins[key][indices[-1]] = rows_into_columns(level_file.readlines())

        #######################################################################
        print('Loading links...')
        with open(join(self.config.data_dir, 'dda_graph.json')) as f:
            graph = json.load(f)

        #######################################################################
        print('Testing links')

        count = 0
        for src_str in graph:
            src, src_index = self.__string_to_key_and_index(src_str)
            for dst_str in graph[src_str]:
                dst, dst_index = self.__string_to_key_and_index(dst_str)
                for linker in ['shortest', 'BC-match']:
                    if graph[src_str][dst_str][linker]['percent_playable'] != 1.0:
                        continue
                    
                    if graph[src_str][dst_str][linker]['link'] == None:
                        level = bins[src][src_index] + bins[dst][dst_index]
                    else:
                        level = bins[src][src_index] + \
                                graph[src_str][dst_str][linker]['link'] + \
                                bins[dst][dst_index]

                    if not self.config.gram.sequence_is_possible(level):
                        print('Sequence not possible!')
                        print(f'Source: {src_str}')
                        print(f'Linker: {linker}')
                        print(f'Destination: {dst_str}')
                        print(columns_into_grid_string(level))

                        import sys
                        sys.exit(-1)

                    count += 1


        print(f'\n{count} links tested and no errors found!\n')