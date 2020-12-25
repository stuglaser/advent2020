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

INPUT = 'inputs/input25.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass

def dprint(*args, **kwargs):
    pass
    #print(*args, **kwargs)

A = 1327981
B = 2822615

MOD = 20201227
def xform(subject, loop):
    value = 1
    for _ in range(loop):
        value *= subject
        value = value % MOD

    return value


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]


    aloop = 6481409
    bloop = 3103233

    print('enc from A:', xform(B, aloop))
    print('enc from B:', xform(A, bloop))
    return

    subject = 7
    val = 1
    for i in range(10000000):
        if i % 10000 == 0: print(i)
        val = (val * subject) % MOD
        if val == B:
            print('Found ', B, 'at loop', i + 1)
            break



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
