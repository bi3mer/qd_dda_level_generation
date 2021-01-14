from collections import deque
from random import choices

class NGram():
    __slots__ = ['input_size', 'n', 'grammar']

    def __init__(self, size):
        self.input_size = size - 1
        self.n = size
        self.grammar = {}

    def add_sequence(self, sequence):
        queue = deque([], maxlen=self.input_size)

        for token in sequence:
            if len(queue) == queue.maxlen:
                key = ','.join(queue)
                if key not in self.grammar:
                    self.grammar[key] = { token: 1 }
                elif token not in self.grammar[key]:
                    self.grammar[key][token] = 1
                else:
                    self.grammar[key][token] += 1

            queue.append(token)

    def has_next_step(self, sequence):
        return sequence in self.grammar

    def get_output(self, sequence):
        unigram = self.grammar[sequence]
        return choices(list(unigram.keys()), weights=unigram.values())[0]

    def get_weighted_output(self, sequence):
        if sequence not in self.grammar:
            return None

        unigram = self.grammar[sequence]
        keys = list(unigram.keys())
        keys.sort(key=lambda k: -unigram[k])
        return keys

    def get_unweighted_output(self, sequence):
        if sequence not in self.grammar:
            return None
            
        unigram = self.grammar[sequence]
        return list(unigram.keys())

    def generate(self, input_sequence, size):
        prior = deque(input_sequence, maxlen=self.n - 1)
        prior_val = ','.join(list(prior))
        output = []

        while len(output) < size and self.has_next_step(prior_val):
            new_token = self.get_output(prior_val)
            output.append(new_token)
            prior.append(new_token)

            prior_val = ','.join(list(prior))

        return output

    def sequence_is_possible(self, sequence):
        prior = deque([], maxlen=self.n - 1)

        for token in sequence:
            key = ','.join(prior)
            if len(prior) == prior.maxlen:
                if key not in self.grammar:
                    return False

                if token not in self.grammar[key]:
                    return False

            prior.append(token)

        return True
        