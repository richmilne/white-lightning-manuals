import os
import sys

files = os.listdir('.')
files = [f for f in files if 'cheat' in f or 'manual' in f]
files.sort()

def parse_formatting(line):

    last_code = None
    bold_pos = []
    under_pos = []
    plain_text = []
    stack = []
    offset = 0
    
    state = 0
    for i, c in enumerate(line):
        if state == 0:
            if c in '*_':
                last_code = c
                state = 1
            else:
                plain_text.append(c)
        elif state == 1:
            if c != last_code:
                plain_text.append(last_code)
                last_code = None
            else:
                offset += 2
                if c == '*':
                    bold_pos.append(i+1-offset)
                elif c == '_':
                    under_pos.append(i+1-offset)
                if len(stack) != 0 and stack[-1] == c:
                    stack.pop()
                else:
                    stack.append(c)
            state = 0
            
    assert len(bold_pos) % 2 == 0
    assert len(under_pos) % 2 == 0
    assert len(stack) == 0
    
    bold_pos = [(num, '*') for num in bold_pos]
    under_pos = [(num, '_') for num in under_pos]
    
    markers = bold_pos + under_pos
    markers.sort()
    
    plain_text = ''.join(plain_text)

    return((plain_text, tuple(markers)))
    
def output_text(line):
    return line[0]
    
def output_formatting(line, markup = None):
    if line[1] is None:
        return line[0]
        
    if markup is None:
        markup = {'*': ['**', '**'],
                  '_': ['__', '__']}

    output = []
    stack = [0]
    markers = line[1]
    length = len(markers)
    pointer = 0
    
    for i, c in enumerate(line[0]):
        if i == markers[pointer][0]:
            pos, marker = markers[pointer]
            pointer += 1
            # print 'Match:', pos, marker
            if marker == stack[-1]:
                index = 1
                stack.pop()
            else:
                index = 0
                stack.append(marker)
            output.append(markup[marker][index])

        if pointer == length:
            output.append(line[0][i:])
            break

        output.append(c)

    assert len(stack) in [1, 2]
    if len(stack) == 2:
        output.append(markup[stack[-1]][1])

    return ''.join(output)


html_dict = {'*': ['<b>', '</b>'],
             '_': ['<u>', '</u>']}

for f in files:
    marked = []
    lines = file(f).readlines()
    for line_num, l in enumerate(lines):
        l = l.rstrip()
        if '**' in l or '__' in l:
            try:
                marked.append(parse_formatting(l))
            except:
                print
                print 'Error in file:', f
                print 'At line number:', line_num
                print lines[line_num]
                print
                raise
        else:
            marked.append((l, None))
            
    for m in marked:
        if m[1] is not None:
            print
            print output_formatting(m)
            print output_text(m)
            print output_formatting(m, html_dict)            

