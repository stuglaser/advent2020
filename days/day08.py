#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input08.txt'


class Instr:
    def __init__(self, op, val):
        self.op = op
        self.val = val

    def __repr__(self):
        return f'{self.op} {self.val}'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def run(prog):
    seen = [False] * len(prog)

    pc = 0
    acc = 0
    while True:
        seen[pc] = True

        instr = prog[pc]
        if instr.op == 'acc':
            acc += instr.val
            pc += 1
        elif instr.op == 'jmp':
            pc = pc + instr.val
        elif instr.op == 'nop':
            pc += 1
        else:
            raise Exception('Cannot execute:', instr, '   at ', pc)

        if pc == len(prog):
            return True, acc
        elif pc > len(prog):
            raise Exception('undefined behavior I think')
            return True, acc

        if seen[pc] == True:
            return False, acc



def main():
    # ====== Rule parsing
    prog = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()
            bits = line.split()
            prog.append(Instr(bits[0], int(bits[1])))


    seen = [False] * len(prog)

    pc = 0
    acc = 0
    while True:
        seen[pc] = True

        instr = prog[pc]
        if instr.op == 'acc':
            acc += instr.val
            pc += 1
        elif instr.op == 'jmp':
            pc = pc + instr.val
        elif instr.op == 'nop':
            pc += 1

        if seen[pc] == True:
            break

    print('part 1, acc = ', acc)

    # Try all adjustments
    for i in range(len(prog)):
        mod = None
        if prog[i].op == 'jmp':
            mod = prog[:]
            mod[i] = Instr('nop', prog[i].val)
        elif prog[i].op == 'nop':
            mod = prog[:]
            mod[i] = Instr('jmp', prog[i].val)

        if mod:
            term, acc = run(mod)
            if term:
                print(f'Terminated, part 2 = {acc}  (Adjusted {i} to {mod[i]})')



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
