#! /usr/bin/env python3
# Originally used to uniformly align page numbers in the table of contents.
# Needs reworking now that page numbers are, and sometimes section headers can
# be, surrounded by bold delimiters (**)
import os
import sys

from pathlib import Path

width = 55
offset = 4

basedir = Path(__file__).parent
manual = (basedir / '..' / 'texts' / 'manual').resolve()

for suffix in ['ii', 'iii']:
    name = f'manual_{suffix}.txt'
    lines = [l.rstrip() for l in open(manual / name).readlines()]
    new = False

    for l in lines:
        if l.strip() == '':
            print()
            new = True
            continue

        bits = l.rsplit(' ', 1)
        try:
            # Always throws exception - page numbers now enclosed by **
            page = int(bits[-1])
            page = str(page).rjust(3)
            heading = bits[0].strip()
        except:
            print(l)
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
        print(line)