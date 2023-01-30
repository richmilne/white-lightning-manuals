#! /usr/bin/env python3
import os
import sys

param_width = 18
action_width = 43
param_col = 9
action_col = 28


def split_params(text):

    param_list = []
    param_line = []

    params = [p.strip()+',' for p in text.split(',')]
    params[-1] = params[-1][:-1]

    count = 0
    for p in params:
        count += len(p)
        if count >= param_width:
            param_list.append(''.join(param_line))
            param_line = []
            count = len(p)
        param_line.append(p)
        param_line.append(' ')
        count += 1
    param_list.append(''.join(param_line))
#    print
#    for p in param_list:
#        print p
#    print

    return param_list


def split_actions(text):
    action_list = []
    action_line = []

    if text[-1] != '.':
        text += '.'

    actions = [t.strip() for t in text.split(' ')]
    count = 0
    for a in actions:
        count += len(a)
        if count >= action_width:
            action_list.append(''.join(action_line))
            action_line = []
            count = len(a)
        action_line.append(a)
        action_line.append(' ')
        count += 1
    action_list.append(''.join(action_line))
#    print
#    for a in action_list:
#        print a
#    print

    return action_list


def convert(filename):

    lines = [l.strip() for l in open(filename, 'r').readlines()]

    output = []#'# TODO: Remove this comment once this file has been proofread\n']

    for l in lines:
        bits = [b.strip() for b in l.split('  ') if b != '']
        if len(bits) == 2:
            bits = [bits[0], ' ', bits[1]]
        #print bits
        #continue
        if len(bits) == 3:
            cmd, params, action = bits
            params = split_params(params)
            actions = split_actions(action)
            rows = max([len(params), len(actions)])
            lines = []
            for i in range(rows):
                line = [' ']*83
                lines.append(line)
            lines[0][:len(cmd)] = cmd
            for i, param in enumerate(params):
                lines[i][param_col:param_col+len(param)] = param
            for i, action in enumerate(actions):
                lines[i][action_col:action_col+len(action)] = action

            output.append('')
            for line in lines:
                output.append(''.join(line))
        else:
            output.append(l)

    return output


if __name__ == '__main__':
    for name in sys.argv[1:]:
        lines = convert(name)
        with open(name, 'w') as handle:
            for line in lines:
                handle.write(line)
                handle.write('\n')