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

INPUT = 'inputs/input20.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


MONSTER_STR = '                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '

def find_monsters(canvas):
    # Assuming they don't overlap?
    monster = MONSTER_STR.split('\n')
    H, W = heightwidth(canvas)
    MH, MW = heightwidth(monster)

    monster_pixels = set()
    for r in range(H - MH + 1):
        for c in range(W - MW + 1):
            match = True
            this_monster = []
            for mr in range(MH):
                for mc in range(MW):
                    if monster[mr][mc] == '#':
                        this_monster.append( (r + mr, c + mc) )
                        if canvas[r + mr][c + mc] != '#':
                            match = False

            if match:
                #print('Match at', r, c)
                monster_pixels.update(this_monster)

    if monster_pixels:
        debug_image = []
        for r, row in enumerate(canvas):
            debug_row = ''.join('O' if (r, c) in monster_pixels else char for c, char in enumerate(row))
            print(debug_row)
            debug_image.append(debug_row)


        cnt = 0
        for row in debug_image:
            cnt += sum(1 for c in row if c == '#')
        print('part 2:', cnt)


TILE_SIZE = 10

# Rotations are counter-clockwise steps of 90-degrees
#
# The tile edges are read out in a specific order/direction, which is around the
# tile in a counter-clockwise direction.
#
#       <---------
#     +------------+
#  |  |            |  ^
#  |  |            |  |
#  |  |            |  |
#  |  |            |  |
#  |  |            |  |
#  v  |            |  |
#     +------------+
#       ---------->


def transpose_tile(tile):
    new = []
    for c in range(len(tile[0])):
        new.append(''.join(row[c] for row in tile))
    return new


def rotate_tile_once(tile):
    new = []
    for c in range(len(tile[0]) - 1, -1, -1):
        new.append(''.join(row[c] for row in tile))
    return new


# Functions for reading out the tile edges
def top_of_tile(tile):
    return tile[0]
def right_of_tile(tile):
    return ''.join(line[-1] for line in tile)
def bottom_of_tile(tile):
    return tile[-1][::-1]
def left_of_tile(tile):
    return ''.join(line[0] for line in reversed(tile))


TOP, RIGHT, BOTTOM, LEFT = range(4)
EDGE_STR = {TOP: 'top', RIGHT: 'right', BOTTOM: 'bottom', LEFT: 'left'}
EDGE_GETTERS = [top_of_tile, right_of_tile, bottom_of_tile, left_of_tile]
COMPLEMENT = {TOP: BOTTOM, BOTTOM: TOP, LEFT: RIGHT, RIGHT: LEFT}
STEP_TO = {TOP: Pt(-1, 0), RIGHT: Pt(0, 1), BOTTOM: Pt(1, 0), LEFT: Pt(0, -1)}
class Transform:
    def __init__(self, transpose, rot):
        self.transpose = transpose
        self.rot = rot % 4

    @classmethod
    def identity(Cls):
        return Cls(False, 0)

    def edge_of(self, edge, tile):
        # The dumb way
        transformed = self.apply(tile)
        return EDGE_GETTERS[edge](transformed)

    def apply(self, tile):
        if self.transpose:
            tile = transpose_tile(tile)
        for _ in range(self.rot):
            tile = rotate_tile_once(tile)
        return tile

    def rotated(self, more_rot):
        return Transform(self.transpose, self.rot + more_rot)

    def __repr__(self):
        return f'Tr({self.transpose}, {self.rot})'


def main():
    tiles = {}  # ID -> tile  (`tile` is a list of lines)
    for group in iter_line_groups(INPUT):
        tile_num = int(group[0].split()[1][:-1])
        tiles[tile_num] = group[1:]

    # A placed tile. Tile number, and its transform
    Placement = namedtuple('Placement', ['tile', 'transform'])

    # Lookup the tiles by their edges
    #
    # The transform describes how to get the *top* edge to be the given string.
    by_edge = {}  # {edge_str: [Placement]}
    for num, tile in tiles.items():
        for transpose in (False, True):
            for rot in range(4):
                tr = Transform(transpose, rot)
                edge_str = tr.edge_of(TOP, tile)
                by_edge.setdefault(edge_str, []).append(Placement(num, tr))

    # Part 1 things
    tile_match_count = defaultdict(int)
    for placements in by_edge.values():
        if len(placements) == 2:
            for plc in placements:
                tile_match_count[plc.tile] += 1
    corners = []
    prod = 1
    for tile, matches in tile_match_count.items():
        if matches == 2 * 2:
            corners.append(tile)
            prod *= tile
    print(f'Part 1: {prod}, because corners are {corners}')

    # We can start with any tile
    first_tile = min(tiles.keys())

    layout = {}  # {(row, col) -> Placement}
    layout[Pt(0, 0)] = Placement(first_tile, Transform(False, 0))
    stack = [Pt(0, 0)]
    while stack:
        center = stack.pop()
        tilenum, tr = layout[center]
        tile = tiles[tilenum]

        # Each edge of the current tile
        for edge in range(4):
            match_loc = center + STEP_TO[edge]
            if match_loc not in layout:
                # Pulls out the string for the edge we need to match
                edge_str = tr.edge_of(edge, tile)
                need = edge_str[::-1]

                # Tries to find a tile that matches
                maybe_found = [plc for plc in by_edge[need] if plc.tile != tilenum]
                if maybe_found:
                    found, = maybe_found
                    match_transform = found.transform.rotated(2 - edge)
                    layout[match_loc] = Placement(found.tile, match_transform)
                    stack.append(match_loc)

    # Tile locations are known now. Collects them into a grid

    row_min, row_max = minmax(pt.x for pt in layout.keys())
    col_min, col_max = minmax(pt.y for pt in layout.keys())
    print('rows', row_min, row_max, '  and cols', col_min, col_max)

    tile_grid = []
    for r in range(row_min, row_max + 1):
        tile_grid.append([])
        for c in range(col_min, col_max + 1):
            pt = Pt(r, c)
            tile_num, tr = layout[pt]
            tile_grid[-1].append(tr.apply(tiles[tile_num]))
    print(f'Tile grid is {len(tile_grid)} x {len(tile_grid[0])}')

    # Renders the grid of tiles to the canvas
    canvas = []
    for tile_row in tile_grid:
        #for r in range(TILE_SIZE):
        for r in range(1, TILE_SIZE - 1):
            line = ''
            for tile in tile_row:
                line += tile[r][1:-1]
            canvas.append(line)

    print('\n\nCanvas of composed tiles:')
    print('\n'.join(canvas))
    print(f'\nCanvas is {len(canvas)} x {len(canvas[0])}')


    for transpose in (False, True):
        for rot in range(4):
            tr = Transform(transpose, rot)
            print('\n\nChecking canvas at', tr)
            find_monsters(tr.apply(canvas))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
