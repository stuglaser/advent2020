#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import sys

from utils import *

INPUT = 'inputs/input11.txt'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def step(old):
    new = []

    W = len(old[0])
    H = len(old)
    for i in range(len(old)):
        row = []


        for j in range(W):
            if old[i][j] == '.':
                row.append('.')
            else:
                occ = 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == dj == 0:
                            continue
                        if i + di < 0 or i + di >= H:
                            continue
                        if j + dj < 0 or j + dj >= W:
                            continue

                        if old[i + di][j + dj] == '#':
                            occ += 1

                if occ == 0:
                    row.append('#')
                elif occ >= 4:
                    row.append('L')
                else:
                    row.append(old[i][j])

        new.append(''.join(row))

    return new


OFFSETS = [Pt(1, 0), Pt(1, 1), Pt(0, 1), Pt(-1, 1), Pt(-1, 0), Pt(-1, -1), Pt(0, -1), Pt(1, -1)]
def step2(old):
    new = []

    W = len(old[0])
    H = len(old)
    for i in range(H):
        row = []
        for j in range(W):
            if old[i][j] == '.':
                row.append('.')
            else:
                occ = 0
                center = Pt(i, j)

                for offset in OFFSETS:
                    pt = center
                    while True:
                        pt = pt + offset

                        if pt[0] < 0 or pt[0] >= H or pt[1] < 0 or pt[1] >= W:
                            # Off the grid
                            break

                        ch = old[pt[0]][pt[1]]
                        if ch == '.':
                            pass
                        elif ch == '#':
                            occ += 1
                            break
                        elif ch == 'L':
                            break


                if occ == 0:
                    row.append('#')
                elif occ >= 5:
                    row.append('L')
                else:
                    row.append(old[i][j])

        new.append(''.join(row))

    return new


def compute_visibility(grid):
    vis = []
    H, W = len(grid), len(grid[0])
    for i in range(H):
        vis.append([])
        row = vis[-1]
        for j in range(W):
            row.append([])
            if grid[i][j] == '.':
                row[-1].append(None)
            else:
                center = Pt(i, j)

                for offset in OFFSETS:
                    pt = center
                    while True:
                        pt = pt + offset

                        if pt[0] < 0 or pt[0] >= H or pt[1] < 0 or pt[1] >= W:
                            # Off the grid
                            break

                        ch = grid[pt[0]][pt[1]]
                        if ch == '.':
                            pass
                        elif ch == '#' or ch == 'L':
                            row[-1].append( (pt[0], pt[1]) )
                            break
    return vis


def step2_fast(old, vis):
    new = []
    H, W = len(old), len(old[0])

    for i in range(H):
        row = []
        for j in range(W):
            if old[i][j] == '.':
                row.append('.')
            else:
                occ = 0
                for pt in vis[i][j]:
                    if old[pt[0]][pt[1]] == '#':
                        occ += 1
                if occ == 0:
                    row.append('#')
                elif occ >= 5:
                    row.append('L')
                else:
                    row.append(old[i][j])
        new.append(''.join(row))

    return new


def main():
    grid = []
    with open(INPUT, 'r') as fin:
        for line in fin:
            line = line.rstrip()

            grid.append(line)

    visibility = compute_visibility(grid)

    old = grid
    while True:
        #new = step2(old)
        new = step2_fast(old, visibility)
        if new == old:
            print('DONE!!!')
            occ = 0
            for row in new:
                for c in row:
                    if c == '#':
                        occ += 1

            print('Stable point:', occ)
            break

        old = new


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
