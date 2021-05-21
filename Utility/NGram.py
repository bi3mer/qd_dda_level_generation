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
                key = tuple(queue)
                if key not in self.grammar:
                    self.grammar[key] = { token: 1 }
                elif token not in self.grammar[key]:
                    self.grammar[key][token] = 1
                else:
                    self.grammar[key][token] += 1

            queue.append(token)

    def has_next_step(self, sequence):
        return tuple(sequence) in self.grammar

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
    
    def generate(self, prior, size):
        output = []

        while len(output) < size and self.has_next_step(prior):
            new_token = self.get_output(prior)
            output.append(new_token)
            prior = tuple(prior[-1:]) + (new_token,)

        return output

    def sequence_is_possible(self, sequence):
        prior = deque([], maxlen=self.n - 1)

        for token in sequence:
            key = tuple(prior)
            if len(prior) == prior.maxlen:
                if key not in self.grammar:
                    print(key)
                    return False

                if token not in self.grammar[key]:
                    print(key, token)
                    return False

            prior.append(token)

        return True
        
    def count_bad_n_grams(self, sequence):
        max_length = self.n - 1
        queue = deque([], maxlen=max_length)
        append_to_queue = queue.append
        bad_transitions = 0

        for token in sequence:
            if len(queue) == max_length:
                input_sequence = tuple(queue)
                if input_sequence not in self.grammar:
                    bad_transitions += 1
                elif token not in self.grammar[input_sequence]:
                    bad_transitions += 1

            append_to_queue(token)

        return bad_transitions

    def prune(self):
        pruned = set()

        while True:
            leaves = set()
            for key, val in self.grammar.items():
                if len(val) == 0:
                    leaves.add(key)
                for e in val:
                    if e not in self.grammar:
                        leaves.add(e)

            if len(leaves) == 0:
                return pruned

            for leaf in leaves:
                if leaf in self.grammar:
                    del self.grammar[leaf]

                for key, val in self.grammar.items():
                    if leaf in val:
                        del val[leaf]

            for leaf in leaves:
                pruned.add(leaf)
