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

INPUT = 'inputs/input23.txt'
#INPUT='TEMP'

CUPS = [3, 9, 4, 6, 1, 8, 5, 2, 7]

class TestToday(unittest.TestCase):
    def test_common(self):
        pass

def dprint(*args, **kwargs):
    pass
    #print(*args, **kwargs)



@profile
def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    # Current cup is always 0
    cups = CUPS[:]

    PART = 2

    if PART == 1:
        STEPS = 100
        TOP = max(cups)
        assert len(cups) == max(cups)
    else:
        STEPS = 10000000
        TOP = 1000000


    STEPS=1000000
    after = [i + 1 for i in range(TOP + 1)]
    after[0] = None  # Indexing starts at 1
    after[-1] = cups[0]

    for i in range(len(cups) - 1):
        after[cups[i]] = cups[i + 1]
    after[cups[-1]] = max(cups) + 1 if TOP > max(CUPS) else cups[0]

    at = cups[0]
    for i in range(STEPS):
        #print(f'\nMove {i + 1}  AT {at} (tracking {len(after)})')
        taken_first = after[at]
        taken_middle = after[taken_first]
        taken_last = after[taken_middle]

        place = at - 1 if at > 1 else TOP
        while place in (taken_first, taken_middle, taken_last):
            place -= 1

            if place < 1:
                place = TOP
        #print(f'  Place after {place}, Took {taken_first}, {taken_middle}, {taken_last}')

        # Trims out taken
        after[at] = after[taken_last]

        # Place just after `place`
        after[taken_last] = after[place]
        after[place] = taken_first

        # Advance
        at = after[at]

    if PART == 1:
        flat = []
        at = 1
        while True:
            at = after[at]
            if at == 1:
                break
            flat.append(at)

        print('Part 1:', flat)
    else:
        star1 = after[1]
        star2 = after[star1]
        #print(f'Part 2: {star1} * {star2} = {star1 * star2}')
        print('Part 2: ', star1, '*', star2, '=', star1 * star2)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
