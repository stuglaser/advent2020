#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

INPUT = 'inputs/input01.txt'


class TestToday(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(1, 1)


def main():
    nums = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            if line:
                nums.append(int(line.strip()))


    past = set()
    for n in nums:
        if (2020 - n) in past:
            print(f'Found {n} * {2020 - n} = {n * (2020 - n)}')

        past.add(n)

    pairs = {}
    for i, a in enumerate(nums):
        for j, b in enumerate(nums[i+1:], start=i+1):
            for c in nums[j+1:]:
                if a + b + c == 2020:
                    print(f'Part 2: {a} * {b} * {c} = {a * b * c}')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
