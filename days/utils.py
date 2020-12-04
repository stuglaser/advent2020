#!/usr/bin/env python3
import contextlib

@contextlib.contextmanager
def maybe_open(path):
    if hasattr(path, 'read'):
        yield path
    else:
        with open(path, 'rb') as fin:
            yield fin


class Pt:
    __slots__ = ['x', 'y']
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def dist1(self):
        return abs(self.x) + abs(self.y)

    def __add__(self, other):
        return Pt(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash( (self.x, self.y) )

    def clone(self):
        return Pt(self.x, self.y)

    def __repr__(self):
        return f'Pt({self.x}, {self.y})'

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y
        raise IndexError(f'Cannot index {idx} into Pt')

    def as_tuple(self):
        return (self.x, self.y)


def read_grid_numpy(fin):
    import numpy as np
    rows = []
    for line in fin:
        rows.append(line.strip())
    arr = np.array(rows, dtype=bytes)
    return arr.view('S1').reshape((arr.size, -1))

def read_grid(file):
    grid = []
    with maybe_open(file) as fin:
        for line in fin:
            grid.append(line.strip())
    return grid
