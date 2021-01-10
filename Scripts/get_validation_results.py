import sys
import os

valid_levels = 0
invalid_levels = 0
percents = []

f = open(os.path.join(sys.argv[1], 'data.csv'))
f.readline() # get rid of header
for line in f.readlines():
    _, _, percent, isValid = line.strip().split(',')
    percents.append(float(percent))

    if isValid:
        valid_levels += 1
    else:
        invalid_levels += 1

f.close()

print(f'Valid Levels: {valid_levels}')
print(f'Invalid Levels:  {invalid_levels}')
print(f'Total Levels: {invalid_levels + valid_levels}')
print(f'Mean Percent Completable: {sum(percents) / len(percents)}')
