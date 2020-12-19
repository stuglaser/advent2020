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

    def __mul__(self, value):
        return Pt(self.x * value, self.y * value)

    __rmul__ = __mul__

    def __imul__(self, value):
        self.x *= value
        self.y *= value
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

    def rot90(self, increments):
        """Returns rotated by 90 degree increments."""
        pt = Pt(self.x, self.y)
        increments = increments % 4
        # Just hardcoding all 4
        if increments == 0:
            return self.clone()
        elif increments == 1:
            return Pt(-self.y, self.x)
        elif increments == 2:
            return Pt(-self.x, -self.y)
        elif increments == 3:
            return Pt(self.y, -self.x)

        raise Exception('Not reachable?')

    def l1dist(self):
        return abs(self.x) + abs(self.y)

    @classmethod
    def in_direction(cls, direction):
        if direction == 'E':
            return Pt(1, 0)
        elif direction == 'N':
            return Pt(0, 1)
        elif direction == 'W':
            return Pt(-1, 0)
        elif direction == 'S':
            return Pt(0, -1)

        raise ValueError('Cannot give a point in direction: ' + direction)


DIRECTIONS = ['E', 'N', 'W', 'S']
IDX_OF_DIRECTION = {d: idx for idx, d in enumerate(DIRECTIONS)}


def left_of(direction, increment=1):
    return DIRECTIONS[(IDX_OF_DIRECTION[direction] + increment) % 4]


def right_of(direction, increment=1):
    return DIRECTIONS[(IDX_OF_DIRECTION[direction] - increment) % 4]


def gcd(a, b):
    if b > a:
        a, b = b, a
    if b == 0: return a

    return gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)


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


def iter_line_groups(file):
    with maybe_open(file) as fin:
        group = []
        for line in fin:
            line = line.rstrip()
            if line:
                group.append(line)
            else:
                yield group
                group = []

        if group:
            yield group


def pad_array(arr):
    import numpy as np
    # Should we pad the bottom/top of the array?
    pad_lo = [False for _ in arr.shape]
    pad_hi = [False for _ in arr.shape]
    for n in range(arr.ndim):
        lo_slice = tuple(0 if i == n else None for i in range(arr.ndim))
        pad_lo[n] = np.sum(arr[lo_slice]) > 0

        hi_slice = tuple(-1 if i == n else None for i in range(arr.ndim))
        pad_hi[n] = np.sum(arr[hi_slice]) > 0

    output_shape = [arr.shape[n] + pad_lo[n] + pad_hi[n]
                    for n in range(arr.ndim)]
    output = np.zeros(output_shape, dtype=arr.dtype)

    # Where to place the input inside the output
    set_rect = [slice(int(pad_lo[n]), -1 if pad_hi[n] else None)
                for n in range(arr.ndim)]
    output[tuple(set_rect)] = arr
    return output



def parse_sexp(string):
    return _parse_sexp_helper(_sexp_tokenize(string))


_NON_SYMBOL_CHARS = '() '
def _sexp_tokenize(string):
    symbol_start = None
    for i, c in enumerate(string):
        if string[i] == '(' or string[i] == ')':
            yield string[i]
        elif string[i] == ' ':
            pass
        else: # Symbol character
            if symbol_start is None:
                # Starting a symbol
                symbol_start = i

            is_end = (i == len(string) - 1) or string[i + 1] in _NON_SYMBOL_CHARS
            if is_end:
                yield string[symbol_start:i + 1]
                symbol_start = None


def _parse_sexp_helper(tokens):
    global level
    # Modifies the tokens iterator
    expr = []
    try:
        while True:
            tok = next(tokens)
            if tok == '(':
                subexpr = _parse_sexp_helper(tokens)
                expr.append(subexpr)
            elif tok == ')':
                return expr
            else:  # Symbol
                expr.append(tok)
    except StopIteration:
        pass

    return expr
