#!/usr/bin/env python3
from collections import deque
from collections import namedtuple
import enum
import itertools
import unittest
import re
import sys

import numpy as np

from utils import *

INPUT = 'inputs/input17.txt'
#INPUT='TEMP'


class TestToday(unittest.TestCase):
    def test_common(self):
        pass


def zeros(*args, **kwargs):
    return np.zeros(*args, **kwargs, dtype=np.int32)


def pad_array(arr):
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
    output[set_rect] = arr
    return output


def main():
    with open(INPUT, 'r') as fin:
        lines = [line.rstrip() for line in fin]

    # Puts into an array
    world = np.zeros([1, 1, len(lines), len(lines[0])], dtype=np.int32)
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            world[0][0][i][j] = 1 if lines[i][j] == '#' else 0

    print('START')
    print(world)

    for iteration in range(6):
        print('\n\n===== ', iteration)
        # Pad
        # if np.sum(world[0,:,:,:]) > 0:
        #     world = np.concatenate([zeros([1, world.shape[1], world.shape[2], world.shape[3]]), world], axis=0)
        # if np.sum(world[-1,:,:,:]) > 0:
        #     world = np.concatenate([world, zeros([1, world.shape[1], world.shape[2], world.shape[3]])], axis=0)
        # if np.sum(world[:,0,:,:]) > 0:
        #     world = np.concatenate([zeros([world.shape[0], 1, world.shape[2], world.shape[3]]), world], axis=1)
        # if np.sum(world[:,-1,:,:]) > 0:
        #     world = np.concatenate([world, zeros([world.shape[0], 1, world.shape[2], world.shape[3]])], axis=1)
        # if np.sum(world[:,:,0,:]) > 0:
        #     world = np.concatenate([zeros([world.shape[0], world.shape[1], 1, world.shape[3]]), world], axis=2)
        # if np.sum(world[:,:,-1,:]) > 0:
        #     world = np.concatenate([world, zeros([world.shape[0], world.shape[1], 1, world.shape[3]])], axis=2)
        # if np.sum(world[:,:,:,0]) > 0:
        #     world = np.concatenate([zeros([world.shape[0], world.shape[1], world.shape[2], 1]), world], axis=3)
        # if np.sum(world[:,:,:,-1]) > 0:
        #     world = np.concatenate([world, zeros([world.shape[0], world.shape[1], world.shape[2], 1])], axis=3)
        world = pad_array(world)

        next_world = world.copy()
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                for k in range(world.shape[2]):
                    for l in range(world.shape[3]):

                        # neighbors
                        ncnt = 0
                        for ni in (i - 1, i, i + 1):
                            for nj in (j - 1, j, j + 1):
                                for nk in (k - 1, k, k + 1):
                                    for nl in (l - 1, l, l + 1):
                                        if ni == i and nj == j and nk == k and nl == l:
                                            pass
                                        elif (0 <= ni < world.shape[0] and
                                              0 <= nj < world.shape[1] and
                                              0 <= nk < world.shape[2] and
                                              0 <= nl < world.shape[3]):
                                            ncnt += world[ni, nj, nk, nl]

                        if world[i,j,k,l]:
                            if not (ncnt == 2 or ncnt == 3):
                                next_world[i, j, k, l] = 0
                        else:
                            if ncnt == 3:
                                next_world[i, j, k, l] = 1

        world = next_world
        print('Ater', iteration + 1, 'cycle:', np.sum(world))
        #print(world)

    print('part x:', np.sum(world))



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1] + sys.argv[2:])
    else:
        main()
