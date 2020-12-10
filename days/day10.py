#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input10.txt'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    nums = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()

            nums.append(int(line))


    BUILTIN = max(nums) + 3
    CHARGE = 0
    nums.sort()

    num1 = 0
    num3 = 1

    for i in range(len(nums)):
        last = 0 if i == 0 else nums[i - 1]
        if nums[i] - last == 3:
            num3 += 1
        elif nums[i] - last == 1:
            num1 += 1

    print('part 1:', num1 * num3)


    nums = [0] + nums + [BUILTIN]
    ways = [0] * len(nums)
    ways[0] = 1
    for i in range(1, len(nums)):
        j = i - 1
        while j >= 0 and nums[j] >= nums[i] - 3:
            ways[i] += ways[j]
            j -= 1

    print('part 2:', ways[-1])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
