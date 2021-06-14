from random import seed

class GenerationLevelGraphTest:
    def __init__(self, config, __seed):
        self.config = config
        seed(__seed)

    def run(self, runs):
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