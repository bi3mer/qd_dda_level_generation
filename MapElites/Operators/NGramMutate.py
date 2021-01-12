from Utility import generate_link

from random import normalvariate, random
from math import ceil, floor

class NGramMutate:
    __slots__ = [
        'standard_deviation', 'mutation_values', 'mutation_rate', 
        'max_length', 'gram', 'max_attempts']

    def __init__(self, mutation_rate, gram, max_length, standard_deviation=3, max_attempts=10):
        '''
        max length should be longer than the original strand length.
        '''
        self.standard_deviation = standard_deviation
        self.mutation_rate = mutation_rate
        self.max_length = max_length
        self.max_attempts = max_attempts
        self.gram = gram

    def mutate(self, strand):
        if strand == None:
            return None

        if random() < self.mutation_rate:
            path = None
            attempts = 0
            while path == None and attempts < self.max_attempts:
                attempts += 1

                mid_normal_point = len(strand) / 3
                points = [
                    normalvariate(mid_normal_point, self.standard_deviation),
                    normalvariate(mid_normal_point, self.standard_deviation)
                ]

                s = max(self.gram.n + 1, floor(min(points)))
                e = max(self.gram.n + 1, ceil(max(points)))

                path = generate_link(self.gram, strand[:s], strand[e:], e-s)

            return path[:self.max_length]
        
        return strand
        