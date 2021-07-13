from Utility.NGram import NGram
from Utility.GridTools import columns_into_grid_string, rows_into_columns

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
lvl = rows_into_columns([l.strip() for l in f.readlines()])
f.close()

if args.dungeongram:
    from Config import DungeonGram
    config = DungeonGram
elif args.mario:
    from Config import Mario
    config = Mario
elif args.icarus:
    from Config import Icarus
    config = Icarus

print(columns_into_grid_string(lvl))
print(f'bad n-grams: {config.gram.count_bad_n_grams(lvl)}')
print(f'% playable:  {config.get_percent_playable(lvl)}')
