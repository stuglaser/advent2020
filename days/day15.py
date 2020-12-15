#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import re
import sys

from utils import *

INPUT = 'inputs/input15.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    nums = [int(s) for s in lines[0].split(',')]

    N = 2020
    #N = 30000000
    prevs = {}
    last_seen = None
    for i in range(1, N + 1):
        # Current num
        if i <= len(nums):
            num = nums[i - 1]
        else:
            num = last_seen or 0

        # Prepares for the next iteration
        if num in prevs:
            last_seen = i - prevs[num]
        else:
            last_seen = None

        prevs[num] = i
        #print(f'[{i}] = {num}  (seen already? {last_seen}')

    print('part 1 or 2: ', num)






if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
