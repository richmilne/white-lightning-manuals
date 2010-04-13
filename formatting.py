import os
import sys
import codecs

def sort_file(name):
    roman = ['i', 'ii', 'iii', 'iv']

    pos = name.find('_')
    assert pos > 0
    num = name[pos+1:-4]
    if num in roman:
        num = -100 + roman.index(num)
    else:
        num = int(num)
    return (name[:pos], num)

def list_files(which = 'all'):

    options = ['all', 'cheatsheet', 'manual']
    assert which in options
    index = options.index(which)

    files = os.listdir('.')
    files = [f for f in files if f[-4:].lower() == '.txt']
    if which == 'all':
        files = [f for f in files if options[1] in f or options[2] in f]
    else:
        files = [f for f in files if options[index] in f]

    files.sort(key = sort_file)
    return files

class text_formatter(object):
    def __init__(self):

        self.markup_dict = {'*':  ['', ''],
                            '_':  ['', ''],
                            '<':  '<',
                            '>':  '>',
                            ' ':  ' ',
                            '{':  '{',
                            '}':  '}',
                            '\\': '\\'}
        self.lines = None
        self.extension = '.txt'
        self.header = unichr(65279)    # BOM
        self.footer = ''
        self.line_end = '\n'
        self.page_sep = '\x0c'

    def parse_formatting(self, line):

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

    def load_file(self, filename):

        marked = []
        handle = codecs.open(filename, 'r', encoding='utf-8')
        lines = handle.readlines()
        handle.close()

        for line_num, l in enumerate(lines):
            l = l.rstrip()
            if '**' in l or '__' in l:
                try:
                    marked.append(self.parse_formatting(l))
                except:
                    print
                    print 'Error in file:', filename
                    print 'At line number:', line_num
                    print lines[line_num]
                    print
                    raise
            else:
                marked.append((l, None))

        self.lines = marked

    def encode_char(self, char):
        if ord(char) == 65279:   # BOM
            return ''
        else:
            return char

    def encode_line(self, line):
        output = []
        stack = [0]

        length = 0
        markup = self.markup_dict
        markers = line[1]
        if markers is not None:
            length = len(markers)
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
                if ord(c) > 127:
                    output.append(self.encode_char(c))
                else:
                    output.append(c)
                first_space = False

        while len(stack) > 1:
            output.append(markup[stack[-1]][1])
            stack.pop()

        return ''.join(output)

    def convert_files(self, file_list, file_stub = None, filename = None):
        # If filename is None, each file is converted individually
        # Otherwise, the contents of all files are output as separate
        # pages in the given filename

        first = True
        for i, f in enumerate(file_list):

            self.load_file(f)
            num_lines = len(self.lines)-1

            if first:
                if filename is not None:
                    name = filename
                else:
                    if file_stub is not None:
                        name = file_stub + str(i).zfill(3)
                    else:
                        name = f[:-4]
                    name += self.extension

                out_file = codecs.open(name, encoding='utf-8', mode='w')
                out_file.write(self.header)
                first = False

            for j, line in enumerate(self.lines):
                out_file.write(self.encode_line(line))
                if j < num_lines:
                    out_file.write(self.line_end)

            if filename is None:
                out_file.write(self.footer)
                out_file.close()
                first = True
            else:
                out_file.write(self.page_sep)

        if filename is not None:
            out_file.write(self.footer)
            out_file.close()


class markup_formatter(text_formatter):
    def __init__(self):
        text_formatter.__init__(self)

        self.markup_dict['*'] = ['**', '**']
        self.markup_dict['_'] = ['__', '__']


class rtf_formatter(text_formatter):
    def __init__(self):
        text_formatter.__init__(self)

        self.markup_dict['*'] = ['{\\b ', '}']
        self.markup_dict['_'] = ['{\\ul ', '}']
        self.markup_dict['{'] = '\\{'
        self.markup_dict['}'] = '\\}'
        self.markup_dict['\\'] = '\\\\'

        self.extension = '.rtf'
        self.header = r"""{\rtf1\ansi\deff0
{\fonttbl{\f0 Courier New;}}
{\info{\title White Lightning Manual}{\author Richard Milne}}
\fs18
"""

    #TODO: Do you want to add creation time, and possibly revision number, to the info block?
    # e.g. {\creatim\yr2010\mo4\dy8\hr13\min1}}
        self.footer = '}'
        self.line_end = '\\par\n'
        self.page_sep = '\\page\n'

    def encode_char(self, char):

        replacement_dict = {9617: '#',
                            8595: 'v',
                            9484: '+', 9472: '-', 9516: 'T', 9488: "\\'ac",
                            9474: '|',
                            9500: '+', 9532: '+', 9508: '+',
                            9492: 'L', 9524: '+', 9496: ']',
                            169: 'C',    # Copyright symbol
                            177: '#',    # Plus/Minus sign
                            178: '2',    # To the second power
                            179: '3',    # To the third power
                            }

        char = ord(char)
        if char == 65279:   # BOM
            return ''
        if char not in replacement_dict:
            print "Can't find substitute for char %d. (%s)" % (char, unichr(char))
            replace = '?'
        else:
            replace = replacement_dict[char]

        if char > 255:
            return '\\u%d%s' % (char, replace)
        else:
            return "\\'%s" % hex(char)[2:]


class html_formatter(text_formatter):
    def __init__(self):
        text_formatter.__init__(self)

        self.markup_dict['*'] = ['<b>', '</b>']
        self.markup_dict['_'] = ['<u>', '</u>']
        self.markup_dict['>'] = '&gt;'
        self.markup_dict['<'] = '&lt;'
        self.markup_dict[' '] = '&nbsp;'

        self.extension = '.html'
        self.header = r"""<html>
    <head>
        <meta http-equiv="Content-Style-Type" content="text/css">
        <style type="text/css">
        <!--
        * {font-family: "Courier New", monospace;
           font-size: 18}
        -->
        </style>
   </head>
   <body>
"""
        self.footer = '</body>'
        self.line_end = '<br/>\n'
        self.page_sep = '<!-- New Page -->\n'

    def encode_char(self, char):

        char = ord(char)
        if char == 65279:   # BOM
            return ''
        else:
            return '&#%d;' % char

files = list_files()
outputter = text_formatter()
outputter.convert_files(files)
