from MapElites import MapElites
from Utility import *

from json import dumps as json_dumps
from os.path import join, exists
from os import mkdir
from subprocess import Popen
from BinsPerEpoch import DungeonGramBinsPerEpoch

dg = DungeonGramBinsPerEpoch()
standard_n_search = MapElites(
    dg.start_population_size,
    dg.feature_descriptors,
    dg.feature_dimensions,
    dg.resolution,
    dg.fast_fitness,
    dg.slow_fitness,
    dg.minimize_performance,
    dg.n_population_generator,
    dg.mutator,
    dg.crossover,
    dg.elites_per_bin,
    rng_seed=dg.seed + 8
)
print(standard_n_search.run(dg.fast_iterations, dg.slow_iterations))