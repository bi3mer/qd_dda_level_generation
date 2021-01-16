from Utility import generate_link

from random import normalvariate
from math import floor

class NGramCrossover:
    __slots__ = ['gram', 'min_length', 'max_length', 'standard_deviation', 'max_attempts']

    def __init__(self, gram, min_length, max_length, standard_deviation=3, max_attempts=10):
        self.standard_deviation = standard_deviation
        self.max_attempts = max_attempts
        self.max_length = max_length
        self.min_length = min_length
        self.gram = gram

    def operate(self, parent_1, parent_2):
        '''
        could be improved by having this take in a selector
        '''
        strand_size = min(len(parent_1), len(parent_2))
        paths = [None, None]
        mid_normal_point = strand_size / 3
        attempts = 0

        while paths[0] == None and paths[1] == None and attempts < self.max_attempts:
            attempts += 1
            cross_over_point = floor(normalvariate(mid_normal_point, self.standard_deviation))
            cross_over_point = max(self.gram.n + 1, cross_over_point)

            start = parent_1[:cross_over_point]
            end = parent_2[cross_over_point:]
            p_1 = generate_link(
                self.gram, 
                start, 
                end, 
                max(self.min_length, len(start) + len(end)))

            if p_1 == None:
                continue
            else:
                paths[0] = p_1

            start = parent_2[:cross_over_point]
            end = parent_1[cross_over_point:]
            p_2 = generate_link(
                self.gram, 
                start, 
                end, 
                max(self.min_length, len(start) + len(end)))
            
            if p_2 == None:
                continue
            else:
                paths[1] = p_2

        if paths[0] != None:
            paths[0] = paths[0][:self.max_length]
        if paths[1] != None:
            paths[1] = paths[1][:self.max_length]
        
        return paths
