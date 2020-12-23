#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
from collections import defaultdict
#import enum
import itertools
from itertools import product
import unittest
import re
import sys


from utils import *

INPUT = 'inputs/input22.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass

def dprint(*args, **kwargs):
    pass
    #print(*args, **kwargs)


last_decks = None
level = 0
game = 0
all_results = {}
def play(deck1, deck2):
    global all_results
    global last_decks
    global level
    global game
    game += 1

    input_tuples = (tuple(deck1), tuple(deck2))
    try:
        return all_results[input_tuples]
    except KeyError:
        pass

    #indent = f'L{level:2}{"  " * level}G{game:4} ] '

    # dprint(f'{indent}Starting level {level}')
    # dprint(f'{"  " * level}Deck 1: {deck1}')
    # dprint(f'{"  " * level}Deck 2: {deck2}')
    prev_decks = { input_tuples }
    round = 0
    while deck1 and deck2:
        round += 1
        # dprint(f'{indent}Round {round}')
        # dprint(f'{indent}Round {round} Deck 1: {deck1}')
        # dprint(f'{indent}Round {round} Deck 2: {deck2}')
        top1, deck1 = deck1[0], deck1[1:]
        top2, deck2 = deck2[0], deck2[1:]
        #dprint(f'{indent}Round {round},  {top1} vs {top2}')

        if len(deck1) >= top1 and len(deck2) >= top2:
            level += 1
            winner = play(deck1[:top1], deck2[:top2])
            all_results[ (tuple(deck1[:top1]), tuple(deck2[:top2])) ] = winner
            level -= 1
        elif top1 > top2:
            winner = 1
        else:
            winner = 2

        #dprint(f'{indent}Round {round} winner is player {winner}')
        if winner == 1:
            deck1 = deck1 + [top1, top2]
        else:
            deck2 = deck2 + [top2, top1]

        if (tuple(deck1), tuple(deck2)) in prev_decks:
            last_decks = (deck1, deck2)
            return 1
        prev_decks.add( (tuple(deck1), tuple(deck2)) )

    last_decks = (deck1, deck2)
    return 1 if deck1 else 2



def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]


    deck1 = []
    deck2 = None
    for line in lines:
        if line.startswith('Player'):
            pass
        elif not line:
            deck2 = []
        else:
            if deck2 is None:
                deck1.append(int(line))
            else:
                deck2.append(int(line))


    # print('deck 1:', deck1)
    # print('deck 2:', deck2)


    # while deck1 and deck2:
    #     if deck1[0] == deck2[0]:
    #         raise 'no ties'

    #     if deck1[0] > deck2[0]:
    #         deck1.append(deck1[0])
    #         deck1.append(deck2[0])
    #     else:
    #         deck2.append(deck2[0])
    #         deck2.append(deck1[0])


    #     deck1 = deck1[1:]
    #     deck2 = deck2[1:]
    #     print('deck 1:', deck1)
    #     print('deck 2:', deck2)

    # print('done')
    # print('deck 1:', deck1)
    # print('deck 2:', deck2)

    # deck1 = [9, 2, 6, 3, 1]
    # deck2 = [5, 8, 4, 7, 10]

    # Infinite
    # deck1 = [43, 19]
    # deck2 = [2, 29, 14]

    winner = play(deck1, deck2)
    global last_decks
    deck1, deck2 = last_decks
    score = 0
    for i, x in enumerate(reversed(deck1 or deck2), start=1):
        score += i * x
        print(i, x)
    print('part 1:', score)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
