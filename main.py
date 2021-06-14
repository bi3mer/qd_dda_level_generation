from TheGoodStuff import *
from Config import Mario, Icarus, DungeonGram

import argparse
import sys

parser = argparse.ArgumentParser(description='Level Generation Pipeline.')
parser.add_argument('--seed', type=int, default=0, help='Set seed for generation')
parser.add_argument(
    '--runs', 
    type=int,
    default=10,
    help='Set the # of runs. Walkthrough is the number of walks and average generates it the # of corpuses generated.')

game_group = parser.add_mutually_exclusive_group(required=True)
game_group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
game_group.add_argument('--mario', action='store_true', help='Run Mario')
game_group.add_argument('--icarus', action='store_true', help='Run Icarus')

type_group = parser.add_mutually_exclusive_group(required=True)
type_group.add_argument('--generate-corpus', action='store_true', help='Generate a corpus')
type_group.add_argument('--generate-graph-test', action='store_true', help='Generate a graph with a corpus built from --corpus')
type_group.add_argument('--generate-graph', action='store_true', help='Generate a graph with a corpus built from --corpus')
type_group.add_argument('--walkthrough', action='store_true', help='Walkthrough a graph built with --generate-graph')
type_group.add_argument('--average-generated', action='store_true', help='Generate a set of corpuses to get the average # levels generated.')
type_group.add_argument('--run-flawed-agents', action='store_true', help='Walkthrough graph built with --generate-graph with a set of flawed agents.')
# parser.add_argument('--run-flawed-agents', action='store_true', help='Assumes pipeline already run. Will run flawed agents on the grid.')


args = parser.parse_args()

if args.dungeongram:
    config = DungeonGram
elif args.mario:
    config = Mario
elif args.icarus:
    config = Icarus

if args.generate_corpus:
    gc = GenerateCorpus(config)
    gc.run(args.seed)
elif args.generate_graph_test:
   ggt = GenerateLevelGraphTest(config, args.seed)
   ggt.run()
elif args.generate_graph:
    raise NotImplementedError('generate graph not implemented yet. Work has not shown which linking method is best')
elif args.walkthrough:
    raise NotImplementedError('walkthrough not implemented yet.')
elif args.run_flawed_agents:
    raise NotImplementedError('run flawed agents not implemented yet.')
elif args.average_generated:
    ag = AverageGenerated(config, args.seed)
    ag.run(args.runs)
else:
    parser.print_help(sys.stderr)
    sys.exit(-1)

# pipeline = GenerationPipeline(config, args.only_map_elites)
# pipeline.run(args.seed)

# p = GenerationPipeline(Mario, False)
# p.run()