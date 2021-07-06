from Utility.GridTools import columns_into_grid_string, columns_into_rows
from Optimization import GA
from random import seed

class GenerateGALevels:
    def __init__(self, config, rng_seed=None):
        self.config = config

        if rng_seed != None:
            seed(rng_seed)

    def run(self, num_levels):
        ga = GA(
            self.config.population_generator,
            self.config.crossover,
            self.config.mutate,
            self.config.fitness,
            not self.config.minimize_performance,
            self.config.start_population_size
        )

        result = ga.run(self.config.iterations)
        for i in range(num_levels):
            print(result[i])
            fitness, level = result[i]
            print(f'fitness: {fitness}')
            if self.config.is_vertical:
                print(columns_into_grid_string(columns_into_rows(level)))
            else:
                print(columns_into_grid_string(level))
            print('\n\n')
        