import os
import sys
import codecs

files = os.listdir('.')
files = [f for f in files if 'cheat' in f or 'manual' in f]
files.sort()

files = ['cheat000.txt']

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

def output_formatting(line, markup = None, escape = False):

    output = []
    stack = [0]

    length = 0
    markers = line[1]
    if markers is not None:
        length = len(markers)
        print line[0]
        print markers
    pointer = 0
    first_space = False

    for i, c in enumerate(line[0]):
        while pointer < length and i == markers[pointer][0]:
            pos, marker = markers[pointer]
            pointer += 1
            if marker == stack[-1]:
                index = 1
                stack.pop()
            else:
                index = 0
                stack.append(marker)
            output.append(markup[marker][index])

        if c in ' <>{}\\':
            if c == ' ':
                if not(first_space):
                    first_space = True
                    output.append(c)
                else:
                    output.append(markup[' '])
            else:
                output.append(markup[c])
                first_space = False
        else:
            if escape and ord(c) > 255:
                output.append("\\u" + str(ord(c))+'?')
            else:
                output.append(c)
            first_space = False

    while len(stack) > 1:
        output.append(markup[stack[-1]][1])
        stack.pop()

    return ''.join(output)


markup = {'*':  ['**', '**'],
          '_':  ['__', '__'],
          '<':  '<',
          '>':  '>',
          ' ':  ' ',
          '{':  '{',
          '}':  '}',
          '\\': '\\'}

html_markup = markup.copy()
html_markup['*'] = ['<b>', '</b>']
html_markup['_'] = ['<u>', '</u>']
html_markup['>'] = '&gt;'
html_markup['<'] = '&lt;'
html_markup[' '] = '&nbsp;'

rtf_markup = markup.copy()
rtf_markup['*'] = ['{\\b ', '}']
rtf_markup['_'] = ['{\\ul ', '}']
rtf_markup['{'] = '\\{'
rtf_markup['}'] = '\\}'
rtf_markup['\\'] = '\\\\'

rtf_header = r"""{\rtf1\ansi\adeflang1025
{\fonttbl{\f0 Courier New;}}
{\info{\title White Lightning Manual}{\author Richard Milne}{\creatim\yr2010\mo4\dy8\hr13\min1}}
\fs18
"""

for f in files:
    marked = []
    handle = codecs.open(f, 'r', encoding='utf-8')
    lines = handle.readlines()
    handle.close()
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

    handle = open('output.rtf', 'w')
    handle.write(rtf_header)
    for m in marked:
        handle.write(output_formatting(m, rtf_markup, True))
        handle.write('\\par\n')
    handle.write('}')
    handle.close()

    while False:
        html = output_formatting(m, html_markup)
        if html != m[0]:
            print
            print output_text(m)
            print output_formatting(m, markup)
            print html
            print output_formatting(m, rtf_markup, True)