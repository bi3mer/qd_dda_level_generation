from TheGoodStuff import GenerationPipeline, BinsPerEpoch
from Config import Mario, Icarus, DungeonGram

import argparse

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
group.add_argument('--mario', action='store_true', help='Run Mario')
group.add_argument('--icarus', action='store_true', help='Run Icarus')
parser.add_argument('--only-map-elites', action='store_true', help='Only run up until map-elites graph.')
# parser.add_argument('--run-flawed-agents', action='store_true', help='Assumes pipeline already run. Will run flawed agents on the grid.')
args = parser.parse_args()

if args.dungeongram:
    config = DungeonGram
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

pipeline = GenerationPipeline(config, args.only_map_elites)
pipeline.run()

# p = GenerationPipeline(Mario, False)
# p.run()