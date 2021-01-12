from random import randrange

class TwoFoldCrossover:
    def operate(self, parent_1, parent_2):
        cross_over_point = randrange(0, min(len(parent_1), len(parent_2)))

        return [
            parent_1[:cross_over_point] + parent_2[cross_over_point:],
            parent_2[:cross_over_point] + parent_1[cross_over_point:]
        ]
