#! /usr/bin/env python3
# Adjust the alignment of the definition characteristics in the FORTH glossary.
# Still needed? If so, review padding now that word definitions are formatted.
import os
import sys

from pathlib import Path

basedir = Path(__file__).parent
manual = (basedir / '..' / 'texts' / 'manual').resolve()

width =  60

valid_defs = ['C','C+','C2','CO','E','L','L0','L1','LO','LU','P','U']

for num in range(91, 119):
    name = manual / f'manual_{num:03}.txt'

    lines = open(name).readlines()

    new_lines = []
    dirty = False

    for l in lines:
        def1 = l.strip().rsplit(',')[-1]
        def2 = l.strip().rsplit(' ')[-1]
        if def1 in valid_defs or def2 in valid_defs:
            l = l.rstrip()
            dirty = True
            text, defs = [t.rstrip() for t in l.rsplit(' ', 1)]
            spaces = width - (len(text) + len(defs))
            new_line = '%s%s%s\n' % (text, ' '*spaces, defs)
            new_lines.append(new_line)
            print(new_line)
        else:
            new_lines.append(l)

    if dirty:
        with open(name, 'w') as handle:
            for line in new_lines:
                handle.write(line)