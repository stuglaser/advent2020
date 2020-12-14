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


def lpad(s, ll):
    return ('0' * (ll - len(s))) + s


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

            print('Mask', origmask, '  gives setval ', bin(setval), ' and throughmask', bin(throughmask))
        else:
            assert line.startswith('mem')
            bits = line.split('=')
            addr = int(bits[0][4:-2])
            val = int(bits[1].strip())

            existing = mem.get(addr, 0)
            mem[addr] = (val & throughmask) | setval
            print(f'Set mem[{addr}] = {bin(mem[addr])}')

    ss = 0
    for k, v in mem.items():
        ss += v
    print('part 1: ', ss)


    mem = {}
    for line in lines:
        if line.startswith('mask'):
            mask = line.split('=')[1].strip()
            print('\nMask now: ', mask)
        else:
            assert line.startswith('mem')
            bits = line.split('=')
            addr = int(bits[0][4:-2])
            val = int(bits[1].strip())


            addr_bits = lpad(bin(addr)[2:], BW)
            assert len(addr_bits) == len(mask), f'{addr_bits}  {mask}'
            together = ''
            for i in range(BW):
                if mask[i] == '0':
                    together += addr_bits[i]
                elif mask[i] == '1':
                    together += '1'
                else:
                    together += 'X'

            print(f'Forming solution for {together}')
            cntx = sum(1 for c in together if c == 'X')
            for k in range(2**cntx):
                k_bits = lpad(bin(k)[2:], cntx)
                k_idx = 0
                print(f'for k = {k} = {k_bits}')

                realaddr_bits = ''
                for i in range(BW):
                    if together[i] == 'X':
                        realaddr_bits += k_bits[k_idx]
                        k_idx += 1
                    else:
                        realaddr_bits += together[i]

                realaddr = int(realaddr_bits, 2)
                print(f'realaddr = {realaddr} = {bin(realaddr)}')
                mem[realaddr] = val

    ss = 0
    for k, v in mem.items():
        ss += v
    print('part 2: ', ss)







if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
