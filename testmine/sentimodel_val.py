#!/usr/bin/python
import numpy as np
import sys

OUT_FILE = 'out_senti.npy'

# print len(sys.argv)
if len(sys.argv) == 2:
    OUT_FILE = sys.argv[1]
    
data = np.load(OUT_FILE)

print data


