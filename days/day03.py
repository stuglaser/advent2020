#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

INPUT = 'inputs/input03.txt'


class TestToday(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(1, 1)


def cnt_trees(map, offset):
    W = len(map[0])

    pos = (0, 0)
    cnt = 0
    while True:
        if pos[0] >= len(map):
            break

        if map[pos[0]][pos[1] % W] == '#':
            cnt += 1

        pos = (pos[0] + offset[0], pos[1] + offset[1])

    return cnt


def main():
    items = []
    map = []
    with open(INPUT, 'r') as fin:
        num_valid = 0

        num_valid2 = 0
        for line in fin:
            map.append(line.strip())

    print('part 1: ', cnt_trees(map, (1, 3)))

    mul = 1
    for offset in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        cnt = cnt_trees(map, offset)
        mul *= cnt
    print('part 2:', mul)

    #print(map)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
