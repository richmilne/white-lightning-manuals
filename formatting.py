import os
import sys
import codecs
import pysvn
from datetime import datetime

enums = ['TEXT', 'BOLD', 'UNDER', 'ESC']
enum_chars = [None, '*', '_', '\\']
for i, e in enumerate(enums):
    globals()[e] = i

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
    def __init__(self, title):

        self.markup_dict = {BOLD: ['', ''],
                            UNDER:['', ''],
                            ESC:  '',
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
        self.page_nums = None
        
        self.title = title
        
        client = pysvn.Client()
        # client.update('.')
        info = client.info('.')

        self.rev_num = info['revision'].number
        self.rev_date = datetime.fromtimestamp(info['commit_time'])
        
    def add_text_token(self, tokens, new_token):
        if len(tokens) > 0 and (tokens[-1][0] == new_token[0] == TEXT):
            tokens[-1].extend(new_token[1:])
        else:
            tokens.append(new_token)

    def parse_formatting(self, line):

        # First split the line up into chunks containing only the same type of
        # chars - either text, or runs of either of the three formatting chars.
        last_code = None
        pieces = []
        piece = []

        state = 0
        for c in line:
            if state == 0:
                if c in '\*_':
                    last_code = c
                    state = 1
                    if len(piece) > 0:
                        pieces.append(piece)
                        piece = []

                piece.append(c)

            elif state == 1:
                if c != last_code:
                    pieces.append(piece)
                    piece = []
                    if c in '\*_':
                        last_code = c
                    else:
                        state = 0

                piece.append(c)

        pieces.append(piece)

        # Convert the pieces from the previous step into tokens.
        # A piece consisting of escape backslashes may convert the first
        # character of the next piece into a text token.
        # For runs of formatting chars, only the first or last two chars will
        # be considered a formatting token, and all the other chars will be
        # considered as ordinary text.

        tokens = []
        num_pieces = len(pieces)
        index = 0
        stack = [None]
        # Load stack with dummy value so we can just test for last value; we
        # don't have to test if stack is non-empty before checking last value...

        while index < num_pieces:
            piece = pieces[index]
            index += 1
            if len(piece) == 0:
                continue

            first = piece[0]
            if first not in '\*_':
                self.add_text_token(tokens, [TEXT] + piece)

            elif first == '\\':
                escapes = len(piece)
                if escapes % 2 == 0:
                    evens = escapes / 2
                    odd = False
                else:
                    evens = (escapes-1)/2
                    odd = True

                if evens > 0:
                    for i in xrange(evens):
                        tokens.append([ESC])
                        tokens.append([TEXT, '\\'])

                if odd:
                    if index != num_pieces and pieces[index][0] in '*_':
                        tokens.append([ESC])
                        char = pieces[index].pop(0)
                        tokens.append([TEXT, char])
                    else:
                        self.add_text_token(tokens, [TEXT, '\\'])

            else:
                count = len(piece)
                if count == 1:
                    self.add_text_token(tokens, [TEXT, piece[0]])
                    continue
                elif count == 4:
                    # Either close an open a section of formatting, or open
                    # and close. Either way, it has no effect, so drop.
                    continue

                if first == '*':
                    token = BOLD
                else:
                    token = UNDER
                open = False
                if stack[-1] == token:
                    # This is the closing marker
                    pass
                else:
                    # It's the opening marker. We can't have formatting nested
                    # more than two deep, so we check for this. Remember that
                    # stack starts with dummy value so we have to compare with 3
                    if len(stack) >= 3:
                        print
                        print "Finish previous formatting block before you open another one!"
                        raise AssertionError
                    open = True

                if count == 2:
                    if open:
                        stack.append(token)
                    else:
                        stack.pop()
                    tokens.append([token])

                elif count == 3:
                    if open:
                        stack.append(token)
                        tokens.append([token])
                        tokens.append([TEXT, first])
                    else:
                        stack.pop()
                        self.add_text_token(tokens, [TEXT, first])
                        tokens.append([token])

                else:
                    chars = count - 4
                    tokens.append([token])
                    tokens.append([TEXT] + [first]*chars)
                    tokens.append([token])

        if len(stack) != 1:
            print 'You forgot to close a section of formatting.'
            raise AssertionError

        for i, t in enumerate(tokens):
            if t[0] == TEXT:
                tokens[i] = [TEXT, ''.join(t[1:])]

        return tokens

    def load_file(self, filename):

        marked = []
        handle = codecs.open(filename, 'r', encoding='utf-8')
        lines = handle.readlines()
        handle.close()

        for line_num, l in enumerate(lines):
            l = l.rstrip()
            if '**' in l or '__' in l or '\\' in l:
                try:
                    marked.append(self.parse_formatting(l))
                except:
                    print
                    print 'Error in file:', filename
                    print 'At line number:', line_num+1
                    print lines[line_num]
                    print
                    raise
            else:
                marked.append([[TEXT, l]])

        self.lines = marked
        self.first_line = True

        if self.page_nums is None:
            return

        num_str = filename[:-4].split('_')[1]
        print filename
        if not(48 <= ord(num_str[0]) <= 57) or num_str == '132':
            return

        num = int(num_str)
        num_str = str(num)
        spaces = 82 - len(num_str)

        if num % 2 == 0:
            if self.page_nums is True:
                footer = (' ' * spaces) + num_str
            else:
                footer = num_str
        else:
            if self.page_nums is True:
                footer = num_str
            else:
                footer = (' ' * spaces) + num_str

        num_lines = len(self.lines)
        pad_lines = 64 - num_lines
        self.lines.extend([[[TEXT, ''*83]]]*pad_lines)
        self.lines.append([[TEXT, footer]])

    def encode_char(self, char):
        if ord(char) == 65279:   # BOM
            return ''
        else:
            return char

    def encode_line(self, tokens):
        output = []
        stack = [None]

        length = 0
        markup = self.markup_dict
        first_space = False
        space_toggle = False
        i = -1

        for t in tokens:
            marker = t[0]
            if marker == TEXT:
                for c in t[1]:
                    i += 1
                    if c in ' <>{}\\':
                        if c == ' ':
                            if not(first_space):
                                first_space = True
                                space_toggle = False

                            if first_space and \
                                       (i == 0 or (i == 1 and self.first_line)):
                                # First space in line, bearing in mind first
                                # char might be BOM
                                space_toggle = True

                            if space_toggle:
                                output.append(markup[' '])
                            else:
                                output.append(c)
                            space_toggle = not(space_toggle)
                        else:
                            output.append(markup[c])
                            first_space = False
                    else:
                        if ord(c) > 127:
                            output.append(self.encode_char(c))
                        else:
                            output.append(c)
                        first_space = False

            elif marker == ESC:
                output.append(markup[ESC])
            else:
                if marker == stack[-1]:
                    index = 1
                    stack.pop()
                else:
                    index = 0
                    stack.append(t[0])
                    pass
                output.append(markup[marker][index])

        self.first_line = False
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

        self.markup_dict[BOLD] = ['**', '**']
        self.markup_dict[UNDER] = ['__', '__']
        self.markup_dict[ESC] = '\\'


class rtf_formatter(text_formatter):
    def __init__(self, title):
        text_formatter.__init__(self, title)

        self.markup_dict[BOLD] = ['{\\b ', '}']
        self.markup_dict[UNDER] = ['{\\ul ', '}']
        self.markup_dict[ESC] = ''
        self.markup_dict['{'] = '\\{'
        self.markup_dict['}'] = '\\}'
        self.markup_dict['\\'] = '\\\\'

        self.extension = '.rtf'
        self.footer = '}'
        self.line_end = '\\par\n'
        self.page_sep = '\\page\n'

        self.header = r"""{\rtf1\ansi\deff0\n{\fonttbl{\f0 Courier New;}}"""
        info = ['{\info',
                '{\\author Richard Milne',
                ' (RichMilne AT users DOT noreply DOT github DOT com)}']
        info.append('{\\version%d}' % self.rev_num)
        creation = '{\creatim\yr%d\mo%d\dy%d\hr%d\min%d}' % (
             self.rev_date.year,
             self.rev_date.month,
             self.rev_date.day,
             self.rev_date.hour,
             self.rev_date.minute)
        info.append(creation)
        info.append('{\subject Revision: %d, %s}' % (self.rev_num, str(self.rev_date)[:19]))
        info.append('{\keywords http://www.worldofspectrum.org/infoseekid.cgi?id=0008967}')
        info.append('{\\title %s}' % self.title)
        info.append('}\n\\fs18\n')
        self.header += ''.join(info)

#{\subject Subject field}{\keywords Keywords}{\doccomm This is my comment text}}

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
    def __init__(self, title):
        text_formatter.__init__(self, title)

        self.markup_dict[BOLD] = ['<b>', '</b>']
        self.markup_dict[UNDER] = ['<u>', '</u>']
        self.markup_dict[ESC] = ''
        self.markup_dict['>'] = '&gt;'
        self.markup_dict['<'] = '&lt;'
        self.markup_dict[' '] = '&nbsp;'

        self.extension = '.html'
        self.footer = '</body>'
        self.line_end = '<br/>\n'
        self.page_sep = '\n<div style="page-break-after:always">' + '-'*83 + '</div>\n'
        
        meta = ['<meta http-equiv="Content-Style-Type" content="text/css">']
        meta.append('<meta name="author" description="Richard Milne (RichMilne AT users DOT noreply DOT github DOT com">')
        meta.append('<meta name="version" description="%d">' % self.rev_num)
        meta.append('<meta name="creation" description="%s">' % str(self.rev_date)[:19])
        meta.append('<meta name="host" description="http://www.worldofspectrum.org/infoseekid.cgi?id=0008967">')
        meta.append('<title>%s</title>' % self.title)

        self.header = r"""<html>
    <head>
        %s
        <style type="text/css">
        <!--
        * {font-family: "Courier New", monospace;
           font-size: 11}
        -->
        </style>
   </head>
   <body>
""" % '\n        '.join(meta)

    def encode_char(self, char):

        char = ord(char)
        if char == 65279:   # BOM
            return ''
        else:
            return '&#%d;' % char

for i, book in enumerate(['cheatsheet', 'manual']):
    files = list_files(book)
    title = 'White Lightning Documentation - %s' % book.title()
    for ext in ['rtf', 'html']:
        outputter = globals()['%s_formatter' % ext](title)
        outputter.page_nums = bool(i)
        name = 'WhiteLightning%s.%s' % (book.title(), ext)
        print '='*83
        print name
        print '='*83        
        outputter.convert_files(files, filename = name)