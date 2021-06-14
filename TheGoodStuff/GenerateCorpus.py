from Utility.GridTools import columns_into_grid_string
from MapElites import MapElites
from Utility.Math import *
from Utility import *

from subprocess import call
from os.path import join
from csv import writer
import json

class GenerateCorpus():
    def __init__(self, config):
        self.config = config


    def run(self, seed):
        #######################################################################
        level_dir =  join(self.config.data_dir, 'levels')

        clear_directory(self.config.data_dir)
        make_if_does_not_exist(level_dir)

        #######################################################################
        print('writing config file for graphing')
        config = {
            'data_file': f'{self.config.data_file}_generate_corpus_data.csv',
            'x_label': self.config.x_label,
            'y_label': self.config.y_label,
            'save_file': f'{self.config.save_file}.pdf',
            'title': self.config.title,
            'resolution': self.config.resolution,
            'feature_dimensions': self.config.feature_dimensions
        }

        f = open(f'{self.config.map_elites_config}.json', 'w')
        f.write(json.dumps(config, indent=2))
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
            rng_seed=seed
        )
        gram_search.run(self.config.iterations)

        #######################################################################
        print('Validating levels...')
        valid_levels = 0
        invalid_levels =  0
        fitnesses = []
        bins = gram_search.bins
        f = open(f'{self.config.data_file}_generate_corpus_data.csv', 'w')
        csv_writer = writer(f)
        csv_writer.writerow(self.config.feature_names + ['index', 'performance'])
        
        keys = list(bins.keys())
        for progress, key in enumerate(keys):
            for index, entry in enumerate(bins[key]):
                fitness = entry[0]
                level = entry[1]

                fitnesses.append(fitness)
                if fitness == 0.0:
                    valid_levels += 1
                else:
                    invalid_levels +=1 
                
                csv_writer.writerow(list(key) + [index, fitness])

                level_file = open(join(level_dir, f'{key[1]}_{key[0]}_{index}.txt'), 'w')
                level_file.write(columns_into_grid_string(level))
                level_file.close()

            update_progress(progress / len(keys)) 

        f.close()
        results = {
            'valid_levels': valid_levels,
            'invalid_levels': invalid_levels,
            'total_levels': valid_levels + invalid_levels,
            'fitness': fitnesses,
            'mean_fitness': sum(fitnesses) / len(fitnesses)
        }

        update_progress(1)

        #######################################################################
        print('Storing results and Generating MAP-Elites graph...')
        f = open(join(self.config.data_dir, 'generate_corpus_info.txt'), 'w')
        f.write(json.dumps(results, indent=2))
        f.close()
        
        call(['python3', join('Scripts', 'build_map_elites.py'), self.config.data_dir, str(self.config.elites_per_bin)])
        print('Done!')