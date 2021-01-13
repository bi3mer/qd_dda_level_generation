import json
import sys
import os

f = open(os.path.join(sys.argv[1], 'random_walkthroughs.json'))
data = json.load(f)
f.close()

values = []

for row in data:
    values.append(float(data[row]))

print(f'good paths: {sum([1 for v in values if v == 1.0])} / {len(values)}')
print(f'Average: {sum(values) / len(values)}')