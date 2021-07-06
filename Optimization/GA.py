from random import choices, seed as rng_seed

from Utility import update_progress

class GA:
    def __init__(self, population_generator, crossover, mutate, fitness, maximize, population_size, seed=None):
        self.population_generator = population_generator
        self.crossover = crossover.operate
        self.mutate = mutate.mutate
        self.fitness = fitness
        self.maximize = maximize
        self.population_size = population_size

        if seed != None:
            rng_seed(seed)

    def __add_strand_to_population(self, strand, index, population, population_fitness):
        if index < self.population_size:
            fitness = self.fitness(strand)
            population_fitness[index] = fitness
            population[index] = strand

    def run(self, epochs):
        population = self.population_generator.generate(self.population_size)
        population_fitness = [self.fitness(strand) for strand in population]

        old_population = [strand for strand in population]
        max_fitness = max(population_fitness)
        old_population_fitness = [val if self.maximize else abs(max_fitness - val) for val in population_fitness]

        for e in range(epochs):
            index = 0
            while index < self.population_size:
                parent_1, parent_2 = choices(old_population, weights=old_population_fitness, k=2)
                strands = self.crossover(parent_1, parent_2)
                for strand in strands:
                    self.__add_strand_to_population(self.mutate(strand), index, population, population_fitness)
                    index += 1
            

            old_population = [strand for strand in population]
            max_fitness = max(population_fitness)
            old_population_fitness = [val if self.maximize else abs(max_fitness - val) for val in population_fitness]
            update_progress(e/epochs)

        update_progress(1)
        return [(fitness, lvl) for fitness, lvl in sorted(zip(population_fitness, population), reverse=self.maximize)]
