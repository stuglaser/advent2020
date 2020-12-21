#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
from collections import defaultdict
import enum
import itertools
from itertools import product
import unittest
import re
import sys


from utils import *

INPUT = 'inputs/input21.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass



def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    foods = []
    all_ingredients = set()
    all_allergens = set()
    for line in lines:
        bits = line.split(' (')
        ingredients = bits[0].split()
        allergen_str = bits[1][9:-1] if len(bits) > 1 else None
        allergens = allergen_str.split(', ')

        foods.append( (ingredients, allergens) )
        all_ingredients.update(ingredients)
        all_allergens.update(allergens)

    allergen_isects = {a: all_ingredients for a in all_allergens}
    for ingrs, allers in foods:
        for a in allers:
            allergen_isects[a] = allergen_isects[a].intersection(ingrs)

    assigns = {}  # ingredient -> allergen
    while len(assigns) < len(all_allergens):
        for a in all_allergens:
            allergen_isects[a] = allergen_isects[a] - assigns.keys()
            if len(allergen_isects[a]) == 1:
                ingr = allergen_isects[a].pop()
                print(f'Assigning {a} to {ingr}')
                assigns[ingr] = a
    print()

    safe_ingrs = all_ingredients - assigns.keys()
    cnt = 0
    for ingrs, allers in foods:
        for i in ingrs:
            if i in safe_ingrs:
                cnt += 1
    print('part 1', cnt)


    stuff = list(assigns.items())
    stuff.sort(key=lambda pair: pair[1])
    print('part 2')
    print(','.join(pair[0] for pair in stuff))



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
