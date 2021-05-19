from Utility.LinkerGeneration import generate_link_bfs
from random import randrange, random

class NGramMutate:
    __slots__ = [
        'standard_deviation', 'mutation_values', 'mutation_rate', 
        'max_length', 'gram', 'max_attempts']

    def __init__(self, mutation_rate, gram, max_length, max_attempts=10):
        '''
        max length should be longer than the original strand length.
        '''
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
                point = randrange(self.gram.n, len(strand) - self.gram.n)
                start =  strand[:point]
                end = strand[point + 1:]
                path = start + generate_link_bfs(self.gram, start, end, 1) + end

            if path == None:
                return None
            return path[:self.max_length]
        
        return strand
        