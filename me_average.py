from BinsPerEpoch import MarioBinsPerEpoch, DungeonGramBinsPerEpoch, IcarusBinsPerEpoch
import argparse

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser(description='Generate Multiple Runs of QD')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
group.add_argument('--mario', action='store_true', help='Run Mario')
group.add_argument('--icarus', action='store_true', help='Run Icarus')
parser.add_argument('--runs', type=check_positive, help='Number of runs.', required=True)
parser.add_argument('--seed', type=int, help='Random seed.', default=0)
args = parser.parse_args()

if args.dungeongram:
    runner = DungeonGramBinsPerEpoch()    
elif args.mario:
    runner = MarioBinsPerEpoch()
elif args.icarus:
    runner = IcarusBinsPerEpoch()

runner.seed = args.seed

runner.run(args.runs)
