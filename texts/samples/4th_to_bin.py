#! /usr/bin/env python3
import re
import sys
from pathlib import Path

screen_no_re = re.compile('SCR #([ 0-9]\\d)')

sample_screen = r"""
# Comments are ignored

 ┌─┬───┤SCR # 6├────────────────────────────────────────────────────┐
 │0│: SETUP 0 COL ! 6 ROW ! 24 SPN ! CLS PUTBLS 2 HGT ! 32 ROW ! ;  │
 │1│: LEFT WRL1V ; : RIGHT WRR1V ;                                  │
 │2│: KEYS 1 1 KB IF LEFT ENDIF 8 1 KB IF RIGHT ENDIF ;             │
 │3│: TESTA ATTOFF SETUP BEGIN KEYS 8 2 KB UNTIL ;                  │
 │4│: TESTB ATTOFF EXX SETUP EXX ' KEYS INT-ON ;                    │
 │5│                                                                │
 │6│                                                                │
 │7│                                                               .│
 └─┴────────────────────────────────────────────────────────────────┘

"""


def add_line(new_lines_, new_line_):
    nl = ''.join(new_line_).rstrip()
    if nl.strip():
        new_lines_.append(nl)
    return [], 0


def format_line(line_no, line, width=32):
    new_lines = []
    new_line = [f'  {line_no} ']
    line_len = len(new_line[0])

    for i, c in enumerate(line):
        if line_len >= width:
            new_line, line_len = add_line(new_lines, new_line)
        new_line.append(c)
        line_len += 1
    add_line(new_lines, new_line)

    for line in new_lines:
        text = ''.join(line).rstrip()
        print('|', end='')
        print(text, end='')
        print(' '*(32-len(text)), end='')
        print('|')


def list_block(screen_no, lines):
        print()
        # print(f'SCR # {screen_no:2d}')
        print(f'|SCR # {screen_no}')
        for i, line in enumerate(lines):
            # print(repr(line))
            format_line(i, line)


def parse_block(block):
    lines = [line.strip() for line in block.split('\n')]
    lines = [line for line in lines if line.strip() and not line[0] == '#']
    if not lines:
        return

    assert len(lines) == 10
    assert all([len(l)==68 for l in lines])
    match = screen_no_re.search(lines[0])
    assert match
    screen_no = int(match.group(1))

    lines = [l[3:-1] for l in lines[1:-1]]
    if 1:
        list_block(screen_no, lines)
    return screen_no, lines

if __name__ == '__main__':
    input = Path(sys.argv[1]).absolute().resolve()
    base, ext = input.stem, input.suffix
    output = Path(base + '.bin')

    blocks = open(input).read().split('\n\n')
    all_lines = []
    for block in blocks:
        tup = parse_block(block)
        if not tup: continue
        scr_no, lines = tup
        all_lines.extend(lines)

    with open(output, 'w') as handle:
        for line in all_lines:
            handle.write(line)