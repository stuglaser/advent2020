#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input04.txt'


class TestToday(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(1, 1)


NEED = 'byr iyr eyr hgt hcl ecl pid'.split()
HEX = '0123456789abcdef'
DIGITS = '0123456789'
def passport_is_valid(passport):
    for n in NEED:
        if n not in passport:
            return False

    try:
        byr = int(passport['byr'])
        if byr < 1920 or byr > 2002:
            return False
        iyr = int(passport['iyr'])
        if iyr < 2010 or iyr > 2020:
            return False
        eyr = int(passport['eyr'])
        if eyr < 2020 or eyr > 2030:
            return False
        hgt = passport['hgt']
        if hgt[-2:] == 'cm':
            h = int(hgt[:-2])
            if h < 150 or h > 193:
                return False
        elif hgt[-2:] == 'in':
            h = int(hgt[:-2])
            if h < 59 or h > 76:
                return False
        else:
            return False
        hcl = passport['hcl']
        if hcl[0] != '#' or len(hcl) != 7:
            return False
        for c in hcl[1:]:
            #import ipdb; ipdb.set_trace()
            if c not in HEX:
                return False
        pid = passport['pid']
        if len(pid) != 9:
            return False
        for c in pid:
            if c not in DIGITS:
                return False
        if passport['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            return False
    except Exception as ex:
        print('Exception ', ex, '   parsing', passport)
        return False

    return True


def main():
    passports = []

    num_valid = 0
    num_valid2 = 0
    with open(INPUT, 'r') as fin:
        group = []
        for line in fin:
            line = line.strip()
            if line:
                group.extend(line.split())
            else:
                passport = {}
                for kv in group:
                    k, v = kv.split(':')
                    passport[k] = v

                is_valid = all(n in passport for n in NEED)
                if is_valid:
                    num_valid += 1
                else:
                    pass

                if passport_is_valid(passport):
                    num_valid2 += 1

                group = []


        passport = {}
        for kv in group:
            k, v = kv.split(':')
            passport[k] = v
        if all(n in passport for n in NEED):
            num_valid += 1
        if passport_is_valid(passport):
            num_valid2 += 1

    print('part 1:', num_valid)
    print('part 2:', num_valid2)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
