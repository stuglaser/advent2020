#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
from collections import defaultdict
#import enum
import itertools
from itertools import product
import unittest
import re
import sys


from utils import *

INPUT = 'inputs/input24.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass

def dprint(*args, **kwargs):
    pass
    #print(*args, **kwargs)

OFFSETS = {'e': Pt(1, 0), 'w': Pt(-1, 0),
           'sw': Pt(-1, -1), 'se': Pt(0, -1),
           'nw': Pt(0, 1), 'ne': Pt(1, 1)}


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]


    state = {}
    for line in lines:
        steps = []
        i = 0
        while i < len(line):
            if line[i] in ('n', 's'):
                steps.append(line[i:i + 2])
                i += 2
            else:
                steps.append(line[i])
                i += 1

        at = Pt(0, 0)
        for step in steps:
            at += OFFSETS[step]
        state[at] = 1 - state.get(at, 0)

    print('Part 1:', sum(state.values()))
    print()

    for day in range(100):
        black_neighbors = defaultdict(int)
        for pt, is_black in state.items():
            if is_black:
                for off in OFFSETS.values():
                    black_neighbors[pt + off] += 1

        new_state = {}
        for pt, cnt in black_neighbors.items():
            if state.get(pt, 0) == 0:  # White tile
                if cnt == 2:
                    new_state[pt] = 1
        for pt, is_black in state.items():
            if is_black:
                cnt = black_neighbors[pt]
                if cnt == 0 or cnt > 2:
                    pass
                else:
                    new_state[pt] = 1

        state = new_state

        print(f'After day {day + 1}: {sum(state.values())} black tiles')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
