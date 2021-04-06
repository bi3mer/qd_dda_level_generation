import matplotlib.pyplot as plt 
import json
import sys
import os

print(f'Building {sys.argv[2]}')

f = open(sys.argv[1], 'r')
counts = json.load(f)
f.close()

X = [x for x in range(len(counts['standard']))]
plt.plot(X, counts['standard'], label='Standard')
plt.plot(X, counts['standard_n'], label='Standard + N')
plt.plot(X, counts['genetic'], label='Genetic')

plt.title('Valid Strands Per Generation')
plt.xlabel('Generation')
plt.ylabel('Valid Strands')
plt.legend()
plt.savefig(sys.argv[2])