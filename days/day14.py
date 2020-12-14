#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import re
import sys

from utils import *

INPUT = 'inputs/input14.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    mem = {}
    BW = 36
    for line in lines:
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
            origmask = mask
            assert len(mask) == BW

            throughmask = 0
            setval = 0
            for _ in range(BW):
                throughmask = throughmask << 1
                setval = setval << 1
                if mask[0] == '0':
                    setval += 0  # nop
                elif mask[0] == '1':
                    setval += 1
                else:
                    assert mask[0] == 'X'
                    throughmask += 1

                mask = mask[1:]
        else:
            assert line.startswith('mem')
            bits = line.split('=')
            addr = int(bits[0][4:-2])
            val = int(bits[1].strip())

            existing = mem.get(addr, 0)
            mem[addr] = (val & throughmask) | setval
            #print(f'Set mem[{addr}] = {bin(mem[addr])}')

    print('Part 1: ', sum(mem.values()))


    # ==================== Part 2

    mem = {}
    for line in lines:
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
        else:
            # Bad parsing code
            assert line.startswith('mem')
            bits = line.split('=')
            addr = int(bits[0][4:-2])
            val = int(bits[1].strip())

            # The X's are filled in from `k`
            cntx = sum(1 for c in mask if c == 'X')
            for k in range(2**cntx):
                realaddr = 0
                for b in range(BW):
                    m = mask[BW - b - 1]
                    if m == '0':
                        realaddr += addr & (1 << b)
                    elif m == '1':
                        realaddr += 1 << b
                    else: # X
                        realaddr += (k & 1) << b
                        k = k >> 1

                mem[realaddr] = val

    print('Part 2: ', sum(mem.values()))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
