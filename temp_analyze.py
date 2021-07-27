from json import load
from Config import Mario
from os.path import join

NO_LINK = 'no_link'
FIRST = 'first'
BEST = 'best'
L = 'links'
BC = 'behavioral_characteristics'
C  = 'completability'
CS = 'connection_success'
CE = 'connection_error'
S = 'segments'
R = 'runs'


f = open(join(Mario.data_dir, 'random_walkthrough_results.json'))
stats = load(f)
f.close()

for k in stats['2']:
    print(k)