from itertools import repeat
from random import choice


class NGramPopulationGenerator:
    __slots__ = ['strand_size', 'gram']

    def __init__(self, n_gram, strand_size):
        self.strand_size = strand_size
        self.gram = n_gram

    def generate(self, n):
        return [
            self.gram.generate(choice(list(self.gram.grammar.keys())).split(','), self.strand_size) 
            for _ in repeat(None, n)
        ]
