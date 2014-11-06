#!/usr/bin/python
import re
import sys

if len(sys.argv) != 2:
    print "Note: no string for processing"
    sys.exit(1)

s = sys.argv[1]

m = re.search('\d+x\d+\+0\+0', s)
if not m:
    sys.exit(1)
s = m.group(0)

start = s.find("x") + 1
end = s.find("+")

hstr = s[start : end]
height = int(hstr) - 10

s = s.replace("x%s+" % hstr, "x%d+" % height)

print s
