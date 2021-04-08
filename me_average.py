from BinsPerEpoch import MarioBinsPerEpoch, DungeonGramBinsPerEpoch
import argparse
import sys

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

parser = argparse.ArgumentParser(description='Generate Multiple Runs of QD')
parser.add_argument('--dungeongram', action='store_true', help='Run DungeonGrams')
parser.add_argument('--mario', action='store_true', help='Run Mario')
parser.add_argument('--runs',type=check_positive, help='Number of runs.')

args = parser.parse_args()

if not args.mario and not args.dungeongram and not args.runs:
    parser.print_help()
    sys.exit(0)

if args.dungeongram:
    runner = DungeonGramBinsPerEpoch()    
elif args.mario:
    runner = MarioBinsPerEpoch()

runner.run(args.runs)