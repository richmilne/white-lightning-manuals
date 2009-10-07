import os
import sys

lines = file('glossary.txt').readlines()
output = ['# TODO: Remove this comment once this file has been proofread\n']
for line in lines[:45]:
    output.append(line.rstrip())
lines = lines[45:]

commands = []
block = []

valid_defs = ['C','C+','C2','CO','E','L','L0','L1','LO','LU','P','U']

def extract_def(line):

    temp = line.replace(' ','')
    count = 0
    for i in xrange(len(temp)-1, -1, -1):
        c = temp[i]
        count += 1
        if c == ',': count = 0
        if count == 3:
            i += 1
            break

    def_text = temp[i:]
    defs = []
    if def_text != '':
        bits = def_text.split(',')
        for bit in bits:
            if bit in valid_defs:
                if 'O' in bit:
                    bit.replace('O', '0')
                defs.append(bit)
            else:
                if len(bit) == 2:
                    if bit[1] in valid_defs:
                        defs.append(bit[1])

    defs = ','.join(defs)

    pos = len(line)
    temp = line.lower()
    if defs != '':
        pos = temp.rfind(defs[0].lower())
        assert pos > -1

    return (defs, line[:pos])

def format_stack(text):
    # For evey stack notation in line, break the note into the before and after
    # parts

    stack_notes = []

    new_line = []
    div = False
    for c in text:
        if c == '-':
            if div is False:
                new_line.append('-')
                div = True
        else:
            div = False
            double_space = False
            new_line.append(c)

        if c == ')':
            stack = ''.join(new_line)
            stack_notes.append(stack)
            new_line = []

    if len(new_line) != 0:
        stack_notes.append(''.join(new_line))

    new_stacks = []
    for stack in stack_notes:
        new_stack = []
        if stack.strip() == '': continue
        bits = stack.split(' ')
        bits = [b.strip() for b in bits]
        bits = [b for b in bits if b != '']
        div = bits.index('-')
        new_stack = (' '.join(bits[:div]), ' '.join(bits[div+1:]))
        new_stacks.append(new_stack)

    return new_stacks

def parse_header(line):
    # Parse a header line to extract the command name, the stack diagram, and
    # the definition characteristics
    cmd = ''
    stack = ''
    defs = ''

    if line == 'DO ... +LOOP':
        return (['DO ... +LOOP'], '', [])

    pos = line.find(' ')
    if pos < 0:
        # No spaces; only the command
        cmd = line.strip()
    else:
        cmd = line[:pos]
        defs, stack = extract_def(line[pos:])

    stack = format_stack(stack)
    return cmd, defs, stack
    
def extract_sentences(block):
    sentences = []
    sent = []
    for line in block:
        if len(line) > 8:
            temp = line[8:]
            if temp[0] == ' ':
                sentences.append(' '.join(sent))
                sentences.append(temp)
                sent = []
            else:
                sent.append(temp)
        else:
            sentences.append(' '.join(sent))
            sentences.append(' ')
            sent = []

    sentences.append(' '.join(sent))
    
    new_sentences = []
    for sent in sentences:
        new_sent = []
        bits = sent.split(' ')
        try:
            for bit in bits:
                new_sent.append(bit)
                if len(bit) > 0 and bit[-1] == '.':
                    new_sent.append('')
        except:
            print 'Bits:', bits
            print 'Sent:', sent
            print 'Bit:', bit
            raise
        new_sentences.append(' '.join(new_sent))

    return new_sentences

blanks = 0
for line in lines:
    line = line.rstrip()
    if line == '':
        blanks += 1
    else:
        blanks = 0
    if blanks == 2:
        while block[0].strip() == '':
            block.pop(0)
        while block[-1].strip() == '':
            block.pop()
        if len(block) != 0:
            commands.append(block)
        block = []
        continue
    block.append(line)

line_length = 83
stack_centre = 23

page = 91
page_divisors = ['#', '(ABORT)', '+!', '-FIND', '0<', ';CODE', '>R', 'ABORT', 'BEGIN', 'C,', 'COUNT', 'DEFINITIONS', 'DP', 'ENCLOSE', 'EXECUTE', 'HLD', 'INDEX', 'LIT', 'MESSAGE', 'OUT', 'R', 'S0', 'TASK', 'U/', 'VOCABULARY', 'WORD', 'NOOP']

for block in commands:
    cmds = []
    stacks = []
    defs = ''
    while block[0][0] != ' ' or '--' in block[0]:
        line = block.pop(0)
        cmd, d, st = parse_header(line)
        cmds.append(cmd)
        if d != '':
            assert defs == ''
            defs = d
        stacks.extend(st)
        
    if len(cmds) > 0 and cmds[0] in page_divisors:
        name = 'manual_%s.txt' % str(page).zfill(3)
        handle = open(name, 'w')
        for line in output:
            handle.write(line)
            handle.write('\n')
        handle.close()
        output = ['# TODO: Remove this comment once this file has been proofread\n']
        page += 1

    num_lines = max([len(cmds), len(stacks)])
    lines = []
    for i in xrange(num_lines):
        lines.append([' ']*line_length)

    for i, stack in enumerate(stacks):
        first_len = len(stack[0])+1
        stack_text = ' --- '.join(stack)
        stack_len = len(stack_text)
        start = stack_centre - first_len
        end = start + stack_len
        lines[i][start:end] = stack_text

    for i, cmd in enumerate(cmds):
        lines[i][:len(cmd)] = cmd

    if len(defs) > 0:
        lines[-1][-len(defs):] = defs

    for line in lines:
        output.append(''.join(line))
    output.append('')
        
    sents = extract_sentences(block)
    for sent in sents:
        output.append(sent)
    output.append('')
    output.append('')