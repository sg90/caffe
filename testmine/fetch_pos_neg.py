#!/usr/bin/python
import os

label_file = open("out/label.txt", "r")
os.mkdir("pos")
os.mkdir("neg")
for line in label_file:
    pairstr = line.strip()
    filename, label = pairstr.split()
    if label == "1":
        os.system("cp %s pos" % filename)
    else:
        os.system("cp %s neg" % filename)

label_file.close()