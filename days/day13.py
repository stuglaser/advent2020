#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input13.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    earliest = int(lines[0])
    buses = [int(x) for x in lines[1].split(',') if x != 'x']

    print('Earliest:', earliest)
    print(buses)

    for bus in buses:
        wait = bus - (earliest % bus)
        print('Waiting', wait, 'for bus', bus)

    # 174, bus 29, waiting 6 minutes


    print('\n\n\n')

    departs = [None if x == 'x' else int(x) for x in lines[1].split(',')]
    valids = []  # departs[valids[i]] is a real bus
    for i, x in enumerate(departs):
        if x is not None:
            valids.append(i)


    # base + k * increment == the valid times for all previous buses
    base = valids[0]
    increment = departs[base]
    for idx in valids[1:]:
        print()
        print(f'From {base} + k * {increment}, solving for l * {bus} ~ t + {idx}')
        bus = departs[idx]

        k = 1
        while True:
            if (base + k * increment + idx) % bus == 0:
                break
            k += 1
        t = base + k * increment
        print(f'Found t = {base} + {k} * {increment} = {t}     (({t} + {idx}) % {bus} = {(t + idx) % bus})')

        base = k * increment + base
        increment = lcm(increment, bus)

    t = base
    print()
    print('part 2 =', t)
    print('Final check')
    for i, n in enumerate(departs):
        if n is not None:
            print(f'..  ({t} + {i}) % {n} = {(t + i) % n}')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
