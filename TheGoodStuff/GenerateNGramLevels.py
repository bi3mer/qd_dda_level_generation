from itertools import repeat
from random import seed, choice
from Utility import columns_into_grid_string, columns_into_rows

class GenerateNGramLevels:
    def __init__(self, config, rng_seed):
        self.config = config

        if rng_seed != None:
            seed(rng_seed)

    def run(self, levels_to_generate):
        keys = list(self.config.gram.grammar.keys())

        for _ in repeat(None, levels_to_generate):
            level = self.config.gram.generate(choice(keys), self.config.max_strand_size) 
            if self.config.is_vertical:
                print(columns_into_grid_string(columns_into_rows(level)))
            else:
                print(columns_into_grid_string(level))
            print()
            print()