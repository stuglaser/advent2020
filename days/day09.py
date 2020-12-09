#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input09.txt'

INVALID = 400480901


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def is_sum(prev_list, prev_set, n):
    for k in prev_list:
        if n == 2 * k:
            print('possible dup?', n, k)
        elif n - k in prev_set:
            assert n != 2 * k, f'{n} {k}'
            return True

    return False


def main():
    nums = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()
            nums.append(int(line))

    prev_set = set(nums[:25])
    for i in range(25, len(nums)):
        prev_list = nums[i - 25:i]
        if not is_sum(prev_list, prev_set, nums[i]):
            print('part 1:', nums[i])

        prev_set.remove(nums[i - 25])
        prev_set.add(nums[i])


    for i in range(len(nums)):
        sum = nums[i]
        for j in range(i + 1, len(nums)):
            sum += nums[j]
            if sum == INVALID:
                lo = min(nums[i:j + 1])
                hi = max(nums[i:j + 1])

                print('part 2 = ', lo + hi)

            if sum > INVALID:
                break




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
