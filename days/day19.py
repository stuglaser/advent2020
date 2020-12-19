#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
from itertools import product
import unittest
import re
import sys

from utils import *

INPUT = 'inputs/input19.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    rules_phase = True
    rules = {}
    messages = []
    for line in lines:
        if rules_phase:
            if not line:
                rules_phase = False
            else:
                lhs, rhs = line.split(': ')
                pred = []
                for phrase in rhs.strip().split(' | '):
                    pieces = []
                    for piece in phrase.strip().split():
                        if piece[0] == '"':
                            pieces.append(piece[1])
                        else:
                            pieces.append(int(piece))
                    pred.append(pieces)

                rules[int(lhs)] = pred
                print(f'RULE {pred}   FROM ', line)


        else:
            messages.append(line)

    def check(msg, rule_num):
        # Returns  offset or None
        # rule_num is a rule number or a string/character
        if not msg:
            return None
        if isinstance(rule_num, str):
            if msg[0] == rule_num:
                return 1
            return None

        rule = rules[rule_num]
        for phrase in rule:
            # TODO: multiple possible correct matches???
            idx = 0
            for piece in phrase:
                offset = check(msg[idx:], piece)
                if offset is None:
                    idx = None
                    break
                else:
                    idx += offset
            if idx is not None:
                return idx  # Match!

        return None # No matches

    cnt = 0
    for msg in messages:
        offset = check(msg, 0)
        if offset == len(msg):
            cnt += 1
    print('Part 1:', cnt)


    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    cnt = 0
    for msg in messages:
        print(f'\n\nMESSAGE', msg)
        n42 = 0
        idx = 0
        while True:  # Eating 42's
            offset42 = check(msg[idx:], 42)
            if offset42 is None:
                # No more 42's
                break
            else:
                n42 += 1
                idx += offset42
                print(f'Found 42 #{n42}, at {msg[:idx]}<<{msg[idx:]}')

                # Check's 31's here
                n31 = 0
                idx31 = idx
                while idx31 != len(msg):
                    offset31 = check(msg[idx31:], 31)
                    if offset31 is None:
                        n31 = None # Nope
                        break

                    idx31 += offset31
                    n31 += 1

                if n31 is not None and n31 > 0 and n31 < n42:
                    # Success!!
                    print(f'MATCHES {msg} with {(n42, n31)}')
                    cnt += 1
                    break

    print('Part 2:', cnt)



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
