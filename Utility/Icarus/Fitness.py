from .SummervilleAgent import percent_completable

def build_slow_fitness_function(grammar):
    def slow_fitness(slices):
        # at this point, Icarus slices should be rows
        bad_transitions = grammar.count_bad_n_grams(slices)

        play_slices = list(slices)
        play_slices.insert(0, '----------------')
        play_slices.insert(0, '################')
        play_slices.append(play_slices[-1])
        play_slices.append(play_slices[-1])

        levelStr = list(reversed(play_slices))
        fitness = percent_completable((1, len(play_slices) - 2, -1), levelStr);

        return bad_transitions + 1 - fitness

    return slow_fitness
