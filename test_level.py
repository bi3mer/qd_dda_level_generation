from Utility.NGram import NGram
from Utility.GridTools import columns_into_rows, rows_into_columns

from Utility import DungeonGram
from Utility import Icarus
from Utility import Mario
import argparse

parser = argparse.ArgumentParser(description='Test Level')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
group.add_argument('--mario', action='store_true', help='Run Mario')
group.add_argument('--icarus', action='store_true', help='Run Icarus')
parser.add_argument('--file',type=str, help='path to level file', required=True)
args = parser.parse_args()

f = open(args.file)
lvl = [l.strip() for l in f.readlines()]
f.close()

if args.dungeongram:
    from BinsPerEpoch.DungeonGramBinsPerEpoch import DungeonGramBinsPerEpoch
    from Utility.DungeonGram.IO import get_levels
    n = 3
    gram = NGram(n)
    levels = get_levels()
    for level in levels:
        gram.add_sequence(level)

    lvl = rows_into_columns(lvl)
    dg = DungeonGramBinsPerEpoch()
    f = lambda lvl: dg.get_fitness(lvl, dg.get_percent_playable(lvl))
elif args.mario:
    from Utility.Mario.Fitness import build_slow_fitness_function
    from Utility.Mario.IO import get_levels
    n = 3
    gram = NGram(n)
    levels = get_levels()
    for level in levels:
        gram.add_sequence(level)

    lvl = rows_into_columns(lvl)
    f = build_slow_fitness_function(gram)
elif args.icarus:
    from Utility.Icarus.Fitness import build_slow_fitness_function
    from Utility.Icarus.IO import get_levels

    n = 2
    gram = NGram(n)
    levels = get_levels()
    for level in levels:
        gram.add_sequence(level)

    lvl = list(reversed(lvl))
    f = build_slow_fitness_function(gram)

print(f(lvl))