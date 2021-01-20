import argparse
from Pipeline import Mario, DungeonGram

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
parser.add_argument('--dungeongram', action='store_true', help='Run dungeon generation pipeline')
parser.add_argument('--mario', action='store_true', help='Run mario generation pipeline')
parser.add_argument('--only-map-elites', action='store_true', help='Only run up until map-elites graph.')
parser.add_argument('--run-flawed-agents', action='store_true', help='Assumes pipeline already run. Will run flawed agents on the grid.')

args = parser.parse_args()

if args.dungeongram:
    pipeline = DungeonGram(args.only_map_elites)
    if args.run_flawed_agents:
        pipeline.run_flawed_agents()
    else:
        pipeline.run()

if args.mario:
    pipeline = Mario(args.only_map_elites)
    if args.run_flawed_agents:
        pipeline.run_flawed_agents()
    else:
        pipeline.run()

if not args.mario and not args.dungeongram:
    parser.print_help()
