#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
from itertools import product
import unittest
import re
import sys

from utils import *

INPUT = 'inputs/input18.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass



# Returns (expression, index)
def parse(string):
    expr = []
    i = 0
    while i < len(string):
        if string[i] == ' ':
            pass
        elif string[i] in '0123456789':
            expr.append(int(string[i]))
        elif string[i] in '+*':
            expr.append(string[i])
        elif string[i] == '(':
            subexpr, offset = parse(string[i + 1:])
            i += offset + 1
            expr.append(subexpr)
        elif string[i] == ')':
            break
        else:
            raise 'wtf'

        i += 1

    return expr, i


def eval1(expr):
    val = 0
    op = '+'
    for e in expr:
        if e == '*' or e == '+':
            op = e
        else:
            rhs = None
            if type(e) == list:
                rhs = eval1(e)
            else:  # Number
                rhs = e
            if op == '+':
                val += rhs
            elif op == '*':
                val *= rhs
            else:
                raise 'op'
            op = None

    return val


def eval2(expr):
    flattened = [eval2(e) if type(e) == list else e for e in expr]

    # Repeated find-replace is pretty goofy, but fast enough for this problem!
    try:
        while True:
            idx = flattened.index('+')
            flattened = flattened[:idx - 1] + [flattened[idx - 1] + flattened[idx + 1]] + flattened[idx + 2:]
    except ValueError:
        pass

    p = 1
    for f in flattened:
        if f != '*':
            p *= f
    return p


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    expressions = [parse(line)[0] for line in lines]

    ss = 0
    for expr in expressions:
        value = eval1(expr)
        #print('-->', value)
        ss += value
    print('part 1:', ss)

    ss = 0
    for expr in expressions:
        value = eval2(expr)
        #print('-->', value)
        ss += value
    print('part 2:', ss)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
