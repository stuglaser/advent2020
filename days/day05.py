#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input05.txt'

ROWS = 128


COL = {col: i for i, col in enumerate(['LLL', 'LLR', 'LRL', 'LRR', 'RLL', 'RLR', 'RRL', 'RRR'])}
def seat_id_for(seat):
    a = 0
    b = 128
    for p in seat[:7]:
        mid = (a + b) // 2
        if p == 'F':
            b = mid
        else:
            a = mid

    assert b == a + 1, f'{a} and {b} for {seat}'
    row = a
    col = COL[seat[7:]]
    return row * 8 + col


def better_seat_id_for(seat):
    n = 0
    for c in seat:
        n = n << 1
        if c == 'B' or c == 'R':
            n += 1
    return n


class TestToday(unittest.TestCase):
    def test_common(self):
        self.assertEqual(seat_id_for('FBFBBFFRLR'), 44*8+5)
        self.assertEqual(better_seat_id_for('FBFBBFFRLR'), 44*8+5)


def main():
    best = -1
    all_ids = []
    with open(INPUT, 'r') as fin:
        seats = []
        for line in fin:
            line = line.strip()
            id = better_seat_id_for(line)
            all_ids.append(id)
            if id > best:
                best = id

    print('Part 1:', best)

    all_ids.sort()
    for i in range(len(all_ids) - 1):
        if all_ids[i] + 1 != all_ids[i + 1]:
            print('Part 2:', all_ids[i] + 1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
