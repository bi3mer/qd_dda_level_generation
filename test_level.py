from Utility.Mario.IO import get_levels
from Utility.Mario.Behavior import *
from Utility.Mario.Fitness import *
from Utility.NGram import NGram
from Utility.GridTools import rows_into_columns

import sys

f = open(sys.argv[1])
lvl = rows_into_columns(f.readlines())
f.close()

n = 3
gram = NGram(n)
levels = get_levels()
for level in levels:
    gram.add_sequence(level)

f = build_slow_fitness_function(gram)
print(f(lvl))