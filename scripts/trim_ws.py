#! /usr/bin/env python3
# Trim spaces from the end of lines, and empty lines from the end of files.
# Tabulate maximum line and file lengths so we can get some sense of how to
# size rendered pages.
import os
import sys

from pathlib import Path

basedir = Path(__file__).parent
texts = (basedir / '..' / 'texts').resolve()

global_width = -1
global_length = -1

files = []
for root, dirs_, files_ in os.walk(texts):
    files.extend([Path(root) / f for f in files_
                  if ('cheatsheet' in f or 'manual' in f)])
files.sort()

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

        # if 'manual' in f.name and temp > 82:
        #     print()
        #     print(f.name)
        #     print(line + '<------')

        trimmed.append(line)
        if line != '':
            length = i

    trimmed = trimmed[:length+1]

    if width > global_width:
        global_width = width
    if length > global_length:
        global_length = length

    lengths.append((f.name, width, length))
    print(f'{f.name:<30} {width:3} {length:3}')

    with open(f, 'w') as handle:
        for i, line in enumerate(trimmed):
            handle.write(line)
            if i < length:
                handle.write('\n')

if files:
    print()
    print(f'{"Maximums:":<30} {global_width:3} {global_length:3}')

    if 1:
        lengths.sort(key = lambda x:x[1])
        print()
        for key in ['cheatsheet', 'manual']:
            print()
            for l in lengths:
                if key in l[0]:
                    print(l)
else:
    print('No input files found.')
