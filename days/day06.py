#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input06.txt'

ROWS = 128



class TestToday(unittest.TestCase):
    def test_common(self):
        pass
        #self.assertEqual(seat_id_for('FBFBBFFRLR'), 44*8+5)
        #self.assertEqual(better_seat_id_for('FBFBBFFRLR'), 44*8+5)


def main():
    best = -1
    all_ids = []

    total_any = 0
    total_all = 0
    for group in iter_line_groups(INPUT):
        nums = {}
        for g in group:
            for letter in g:
                if letter in nums:
                    nums[letter] += 1
                else:
                    nums[letter] = 1

        total_any += len(nums)

        for v in nums.values():
            if v == len(group):
                total_all += 1

    print('part 1:', total_any)
    print('part 2:', total_all)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
