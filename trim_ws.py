import os
import sys

files = os.listdir('.')
files = [f for f in files if f[-4:] == '.txt']
files = [f for f in files if 'cheatsheet' in f or 'manual' in f]
files.sort()

global_width = -1
global_length = -1

lengths = []

for f in files:

    trimmed = []
    width = 0
    length = 0

    lines = [l.rstrip() for l in open(f).readlines()]
    for i, line in enumerate(lines):
        temp = len(line)
        if temp > width:
            width = temp

#        if 'manual' in f and temp > 82:
#            print
#            print f
#            print line + '<------'

        trimmed.append(line)
        if line != '':
            length = i

    trimmed = trimmed[:length+1]
    
    if width > global_width:
        global_width = width
    if length > global_length:
        global_length = length
        
    lengths.append((f, width, length))            
    print '%s %s %s' % (f.ljust(30), str(width).rjust(3), str(length).rjust(3))
    
    handle = open(f, 'wb')
    for i, line in enumerate(trimmed):
        handle.write(line)
        if i < length:
            handle.write('\n')
    handle.close()
    
print
print '%s %s %s' % ('Totals:'.ljust(30), str(global_width).rjust(3), str(global_length).rjust(3))

lengths.sort(key = lambda x:x[1])
print
for key in ['cheatsheet', 'manual']:
    print
    for l in lengths:
        if key in l[0]:
            print l
