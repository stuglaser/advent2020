#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input07.txt'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def main():
    # ====== Rule parsing
    rules = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()
            outer, inner_str = line.split(' bags contain ')

            if inner_str == 'no other bags.':
                rules.append( (outer, []) )
            else:
                inners = inner_str.rstrip('.').split(', ')

                preds = []
                for inner in inners:
                    bits = inner.split()
                    count = int(bits[0])
                    desc = ' '.join(bits[1:-1])
                    preds.append( (count, desc) )

                rules.append( (outer, preds) )

    # Adjacency lists
    reverse = {}
    for r in rules:
        outer = r[0]
        for inner in r[1]:
            reverse.setdefault(inner[1], []).append(outer)

    # dfs
    bags = set()
    B = 'shiny gold'
    look = [B]
    while look:
        b = look.pop()
        if b not in bags:
            bags.add(b)

            for outer in reverse.get(b, []):
                look.append(outer)

    print('Part 1:', len(bags) - 1)


    fwd = {k: v for (k, v) in rules}
    look = [B]
    known = {}
    def helper(bag):
        if bag in known:
            return known[bag]

        cnt = 0
        rule = fwd[bag]
        for n, inner in rule:
            cnt += n * (1 + helper(inner))
        known[bag] = cnt
        return cnt

    print('Part 2:', helper(B))




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
