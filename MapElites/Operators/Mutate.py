from random import choice, randrange, random

class Mutate:
    __slots__ = ['mutation_values', 'mutation_rate']

    def __init__(self, mutation_values, mutation_rate):
        self.mutation_values = mutation_values
        self.mutation_rate = mutation_rate

    def mutate(self, strand):
        if random() < self.mutation_rate:
            strand[randrange(0, len(strand))] = choice(self.mutation_values)
        
        return strand
