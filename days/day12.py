#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input12.txt'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass

DIRS = ['E', 'S', 'W', 'N']
def main():
    commands = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()

            commands.append(line)


    pt = Pt(0, 0)
    facing = 'E'
    for cmd in commands:
        go, amount = cmd[0], int(cmd[1:])
        if go == 'N':
            pt = pt + Pt(0, amount)
        elif go == 'E':
            pt = pt + Pt(amount, 0)
        elif go == 'S':
            pt = pt + Pt(0, -amount)
        elif go == 'W':
            pt = pt + Pt(-amount, 0)
        elif go == 'F':
            if facing == 'N':
                pt = pt + Pt(0, amount)
            elif facing == 'E':
                pt = pt + Pt(amount, 0)
            elif facing == 'S':
                pt = pt + Pt(0, -amount)
            elif facing == 'W':
                pt = pt + Pt(-amount, 0)
            pass
        elif go == 'L':
            idx = DIRS.index(facing)
            idx = (idx + 4 - amount // 90) % 4
            facing = DIRS[idx]
        elif go == 'R':
            idx = DIRS.index(facing)
            idx = (idx + amount // 90) % 4
            facing = DIRS[idx]

    print('part 1:', abs(pt.x) + abs(pt.y))




    ship = Pt(0, 0)
    pt = Pt(10, 1)
    for cmd in commands:
        go, amount = cmd[0], int(cmd[1:])
        if go == 'N':
            pt = pt + Pt(0, amount)
        elif go == 'E':
            pt = pt + Pt(amount, 0)
        elif go == 'S':
            pt = pt + Pt(0, -amount)
        elif go == 'W':
            pt = pt + Pt(-amount, 0)
        elif go == 'F':
            for _ in range(amount):
                ship = ship + pt
        elif go == 'L':
            for _ in range(amount // 90):
                pt = Pt(-pt.y, pt.x)
        elif go == 'R':
            for _ in range(amount // 90):
                pt = Pt(pt.y, -pt.x)

    print('Part 2: ', abs(ship.x) + abs(ship.y))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
