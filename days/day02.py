#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

INPUT = 'inputs/input02.txt'


class TestToday(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(1, 1)


def main():
    items = []
    with open(INPUT, 'r') as fin:
        num_valid = 0

        num_valid2 = 0
        for line in fin:
            bits = line.strip().split()

            lo, hi = bits[0].split('-')
            lo = int(lo)
            hi = int(hi)

            letter = bits[1][0]

            password = bits[2]

            #print(lo, hi, letter, password)

            letter_cnt = 0
            for c in password:
                if c == letter:
                    letter_cnt += 1
            if lo <= letter_cnt and letter_cnt <= hi:
                num_valid += 1


            letter_cnt2 = 0
            if password[lo - 1] != password[hi - 1]:
                if password[lo - 1] == letter or password[hi - 1] == letter:
                    num_valid2 += 1

        print('Part 1, num valid = ', num_valid)
        print('Part 2, num valid = ', num_valid2)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
