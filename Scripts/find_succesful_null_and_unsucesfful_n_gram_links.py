# NOTE: this must be moved to the root folder before use

from Config import Mario as config
from os.path import join
from json import load

f = open(join(config.data_dir, 'random_walkthrough_results.json'))
data = load(f)
f.close()

algorithms = ['null', 'shortest', 'BC-match', 'BC-match-f']

k = '2'

for r in data[k]['runs']:
    if 'null' not in r:
        continue

    if 'bc-match' in r:
        continue

    if 'shortest' in r:
        continue

    print(r['segments'])
    break