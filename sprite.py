import os
import sys

for num in [20, 21, 22]:
    name = 'cheatsheet%d.txt' % num
    lines = [l.strip() for l in open(name).readlines()]
    for l in lines:
        bits = l.split(' ')
        bits = [b for b in bits if b!= '']
        if len(b) == 0:
            print
            continue
        if bits[0][0] not in '01234567890':
            print l
            continue
        else:
            bits = [str(i).rjust(3) for i in map(int, bits)]
            print ' %s   %s  %s   %s     %s      %s       %s      %s     %s     %s   %s   %s   %s   %s   %s   %s   %s' % tuple(bits)
        
#SPRITE   H    L    INK    PAPER    FLASH    BRIGHT    XPOS    YPOS      1     2     3     4     5     6     7     8
#------   -    -    ---    -----    -----    ------    ----    ----      -     -     -     -     -     -     -     -
# 003   001  006   007     000      000       001      001     001     255   227   127   000   060   024   060   126
#' %s   %s  %s   %s     %s      %s       %s      %s     %s     %s   %s   %s   %s   %s   %s   %s   %s'