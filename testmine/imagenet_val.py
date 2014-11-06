#!/usr/bin/python
import numpy as np

OUT_FILE = 'out.npy'

data = np.load(OUT_FILE)

print np.sort(data)[0][-5:]

tops = []
for i in range(5):
    idx = data.argmax()
    print idx
    tops.append(idx)
    data[0][idx] = 0

SYNSETS_FILE = '../data/ilsvrc12/synsets.txt'
SYNSET_WORDS_FILE = '../data/ilsvrc12/synset_words.txt'

# synsets = open(SYNSETS_FILE, 'r')
# sets = [syn[:-1] for syn in synsets.readlines()]
# print sets[0:10]

synwords = open(SYNSET_WORDS_FILE, 'r')
wordsets = synwords.readlines()

'''
for n in tops:
    for line in wordsets:
        if sets[n] in line:
            print line
            break
'''

for n in tops:
    print wordsets[n]

# synsets.close()
synwords.close()
