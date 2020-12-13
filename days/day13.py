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


def gcd(a, b):
    if b > a:
        a, b = b, a
    if b == 0: return a

    return gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)



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


    departs = [None if x == 'x' else int(x) for x in lines[1].split(',')]

    # start = 0
    # while True:

    #     ok = True
    #     for j in range(1, len(departs)):
    #         if departs[j] is not None:
    #             # departs[j] must depart at (start + j)
    #             if (start + j) % departs[j] == 0:
    #                 pass # ok
    #             else:
    #                 ok = False
    #                 break

    #     if ok:
    #         print('Done!', start)

    #     start += departs[0]

    valids = []
    for i, x in enumerate(departs):
        if x is not None:
            valids.append(i)


    print('A check in offsetting assumptions')
    print('\n\n\n')


    # base + k * increment == the valid times for all previous busses
    base = valids[0]
    increment = departs[base]
    for i in range(1, len(valids)):
        # The offsets
        a = valids[i - 1]
        b = valids[i]
        x1 = departs[a]
        x2 = departs[b]

        print()
        print(f'From base = {base} +{increment} ...  with l*{x2} reaching t+{b}')

        k = 1
        while True:
            #if ((k * increment) - base) % x2 == (x2 - b):
            print(f'   check {base} + {k} * {increment} + {b} % {x2} = {base + k * increment + b} % {x2} = {(base + k * increment + b) % x2}')
            if (base + k * increment + b) % x2 == 0:
                break
            k += 1
        t = base + k * increment
        print(f'Found t = {base} + {k} * {increment} = {t}     (({t} + {b}) % {x2} = {(t + b) % x2})')

        base = k * increment + base
        increment = lcm(increment, x2)

    t = base #+ increment
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
