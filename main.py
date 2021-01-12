import argparse
from Pipeline import Mario, DungeonGram

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
parser.add_argument('--dungeongram', action='store_true', help='Run dungeon generation pipeline')
parser.add_argument('--mario', action='store_true', help='Run mario generation pipeline')
parser.add_argument('--standard-operators', action='store_true', help='Use standard operators')
parser.add_argument('--only-map-elites', action='store_true', help='Only run up until map-elites graph.')

args = parser.parse_args()

if args.dungeongram:
    pipeline = DungeonGram(args.standard_operators, args.only_map_elites)
    pipeline.run()

if args.mario:
    pipeline = Mario(args.standard_operators, args.only_map_elites)
    pipeline.run()

if not args.mario and not args.dungeongram:
    parser.print_help()
