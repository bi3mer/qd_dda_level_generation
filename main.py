import argparse
from Pipeline import Mario, DungeonGram, Icarus

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
group.add_argument('--mario', action='store_true', help='Run Mario')
group.add_argument('--icarus', action='store_true', help='Run Icarus')
parser.add_argument('--only-map-elites', action='store_true', help='Only run up until map-elites graph.')
parser.add_argument('--run-flawed-agents', action='store_true', help='Assumes pipeline already run. Will run flawed agents on the grid.')
args = parser.parse_args()

if args.dungeongram:
    pipeline = DungeonGram(args.only_map_elites)
elif args.mario:
    pipeline = Mario(args.only_map_elites)
elif args.icarus:
    pipeline = Icarus(args.only_map_elites)

if args.run_flawed_agents:
    pipeline.run_flawed_agents()
else:
    pipeline.run()
