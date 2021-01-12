import argparse
from Pipeline import Mario, DungeonGram

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
parser.add_argument('--dungeongram', action='store_true', help='Run dungeon generation pipeline')
parser.add_argument('--mario', action='store_true', help='Run mario generation pipeline')
args = parser.parse_args()

if args.dungeongram:
    pipeline = DungeonGram()
    pipeline.run()

if args.mario:
    pipeline = Mario()
    pipeline.run()

if not args.mario and not args.dungeongram:
    parser.print_help()
