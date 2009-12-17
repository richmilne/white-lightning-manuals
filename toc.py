import os
import sys

width = 55
offset = 4

for suffix in ['ii', 'iii']:
    name = 'manual_%s.txt' % suffix
    lines = [l.rstrip() for l in open(name).readlines()]
    new = False

    for l in lines:
        if l.strip() == '':
            print
            new = True
            continue
    
        bits = l.rsplit(' ', 1)
        try:
            page = int(bits[-1])
            page = str(page).rjust(3)
            heading = bits[0].strip()
        except:
            print l
            continue

        line = ''
        if new:
            new = False
        else:
            line += ' ' * offset
        line += heading
        spaces = width - len(line)
        line += ' ' * spaces
        line += page
        print line
