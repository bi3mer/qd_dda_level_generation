# NOTE: this must be moved to the root folder before use

from Config import DungeonGram as dg
from os.path import join
from json import load

f = open(join(dg.data_dir, 'random_walkthrough_results.json'))
data = load(f)
f.close()

algorithms = ['null', 'shortest', 'BC-match', 'BC-match-f']

for key in data:
    try:
        k = int(key)
    except:
        continue

    results = {}
    for alg_name in algorithms:
        results[alg_name] = []

    k = key
    for r in data[k]['runs']:
        for alg_name in algorithms:
            if alg_name not in r:
                continue
            
            if r[alg_name]['completability'] == 1.0:
                continue

            segments = r['segments']
            links = r[alg_name]['links']
            level = []
            for i in range(len(links)):
                level += segments[i].copy() + links[i]
            level += segments[i+1].copy()

            results[alg_name].append(dg.get_percent_playable(level, True))

    print(f'k={k}')
    for alg_name in algorithms:
        print(f'{alg_name}: {sum([c == 1.0 for c in results[alg_name]])} / {len(results[alg_name])}')

    print('==================================')
    print()
