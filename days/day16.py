#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import re
import sys

from utils import *

INPUT = 'inputs/input16.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]


    phase = 'fields'
    fields = []
    mine = None
    nearby = []
    for line in lines:
        if phase == 'fields':
            if line:
                f, nums = line.split(': ')
                both = nums.split(' or ')
                pair1 = both[0].strip().split('-')
                pair2 = both[1].strip().split('-')
                fields.append( (f, list(map(int, pair1)), list(map(int, pair2))) )
            else:
                phase = 'mine'
        elif phase == 'mine':
            if not line:
                phase = 'nearby'
            elif line == 'your ticket:':
                pass
            else:
                mine = list(map(int, line.split(',')))

        elif phase == 'nearby':
            if line == 'nearby tickets:':
                pass
            else:
                nearby.append(list(map(int, line.split(','))))



    ss = 0
    good = []
    for ticket in nearby:
        bad_ticket = False
        for n in ticket:
            for f in fields:
                in_any = False
                if (f[1][0] <= n <= f[1][1] or f[2][0] <= n <= f[2][1]):
                    in_any = True
                    break
            if not in_any:
                bad_ticket = True
                ss += n

        if not bad_ticket:
            good.append(ticket)


    print('part 1', ss)

    cand = [set(f[0] for f in fields) for _ in range(len(fields))]

    # Striking out candidates
    for ticket in good:
        for i, n in enumerate(ticket):
            for f, p1, p2 in fields:
                if p1[0] <= n <= p1[1] or p2[0] <= n <= p2[1]:
                    # Ok
                    pass
                else:
                    # Strike! f is not at position i
                    cand[i].remove(f)


    assigned = {}  # {field: index}
    for _ in range(len(fields)):
        for i, c in enumerate(cand):
            left = c - assigned.keys()
            if len(left) == 1:
                assigned[list(left)[0]] = i

    assert len(assigned) == len(fields), 'Failed to assign some fields to indices!'

    prod = 1
    for f, idx in assigned.items():
        if f.startswith('departure'):
            prod *= mine[idx]

    print('Part 2:', prod)




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
