from Utility.NGram import NGram


print('line')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,3])
gram.add_sequence([3,4])

for group in gram.fully_connect():
    print(group)

print('Tiny Circle')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,1])

for group in gram.fully_connect():
    print(group)

print('Circle')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,3])
gram.add_sequence([3,4])
gram.add_sequence([4,1])

for group in gram.fully_connect():
    print(group)

print('Circle -> leaf')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,3])
gram.add_sequence([3,1])
gram.add_sequence([3,4])

for group in gram.fully_connect():
    print(group)

print('Circle -> Circle + leaf')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,3])
gram.add_sequence([3,1])
gram.add_sequence([3,4])
gram.add_sequence([4,5])
gram.add_sequence([5,4])
gram.add_sequence([5,6])

for group in gram.fully_connect():
    print(group)

print('Circle <-> Circle')
gram = NGram(2)
gram.add_sequence([1,2])
gram.add_sequence([2,3])
gram.add_sequence([3,1])
gram.add_sequence([3,4])
gram.add_sequence([4,3])
gram.add_sequence([4,5])
gram.add_sequence([5,3])

for group in gram.fully_connect():
    print(group)

print('3, line')
gram = NGram(3)
gram.add_sequence([1,2,3])
gram.add_sequence([2,3,4])
gram.add_sequence([3,4,5])
for group in gram.fully_connect():
    print(group)

print('3, circle')
gram = NGram(3)
gram.add_sequence([1,2,3])
gram.add_sequence([2,3,4])
gram.add_sequence([3,4,5])
gram.add_sequence([4,5,1])
gram.add_sequence([5,1,2])
for group in gram.fully_connect():
    print(group)

print('3, circle + leaf')
gram = NGram(3)
gram.add_sequence([1,2,3])
gram.add_sequence([2,3,4])
gram.add_sequence([3,4,5])
gram.add_sequence([4,5,1])
gram.add_sequence([5,1,2])
gram.add_sequence([5,1,3])
for group in gram.fully_connect():
    print(group)


print('DG')
from Utility import DungeonGram

gram = NGram(3)
unigram = NGram(1)
levels = DungeonGram.IO.get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

for group in gram.fully_connect():
    print(group)

print('Mario')
from Utility import Mario

gram = NGram(3)
unigram = NGram(1)
levels = Mario.IO.get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

for group in gram.fully_connect():
    print(group)

print('Icarus')
from Utility import Icarus

gram = NGram(2)
unigram = NGram(1)
levels = Icarus.IO.get_levels()
for level in levels:
    gram.add_sequence(level)
    unigram.add_sequence(level)

for group in gram.fully_connect():
    print(group)