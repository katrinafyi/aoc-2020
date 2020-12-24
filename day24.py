from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day24_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp


E = 'e'
SE = 'se'
SW = 'sw'
W = 'w'
NW = 'nw'
NE = 'ne'

DIRECTION = {
    E: (1, 0),
    SE: (0, 1),
    SW: (-1, 1),
    W: (-1, 0),
    NW: (0, -1),
    NE: (1, -1)
}

def parse_line(line):
    i = 0
    o = []
    while i < len(line):
        c = line[i]
        if c in 'ew':
            x = c
        elif c in 'sn':
            c2 = line[i+1]
            x = c + c2
            i += 1
        i += 1
        o.append(x)
    return o


def parse(lines: List[str]):
    lines = lmap(str.strip,lines)
    o = [] 
    for l in lines:
        o.append(parse_line(l))
    return o

def process(data):
    return

# import hexy
# import numpy as np

WHITE = False
BLACK = True

def solve_1(data, extra):
    blacks = set()
    origin = (0, 0)
    for l in data:
        pos = origin
        for d in l:
            pos = tup_add(pos, DIRECTION[d])
        if pos not in blacks:
            blacks.add(pos)
        else:
            blacks.remove(pos)

    return len(blacks)

def solve_2(data, extra):
    blacks = set()
    origin = (0, 0)
    for l in data:
        pos = origin
        for d in l:
            pos = tup_add(pos, DIRECTION[d])
        if pos not in blacks:
            blacks.add(pos)
        else:
            blacks.remove(pos)

    def neighbours(pos):
        for d in DIRECTION.values():
            yield tup_add(pos, d)

    def count_black(pos):
        x = 0 
        for n in neighbours(pos):
            if n in blacks:
                x += 1
        return x

    for i in range(100):
        to_process = set(blacks)
        for x in blacks:
            to_process.update(neighbours(x))

        to_black = []
        to_white = []

        for pos in to_process:
            if pos in blacks:
                n = count_black(pos)
                if n == 0 or n > 2:
                    to_white.append(pos)
            else:
                if count_black(pos) == 2:
                    to_black.append(pos)

        blacks.update(to_black)
        blacks.difference_update(to_white)
        # print(i, len(blacks))
    return len(blacks)

if __name__ == "__main__":
    with open(INPUT) as f:
        lines = f.readlines()
    data = parse(lines)
    extra = process(data)
    print('sol 1:', solve_1(data, extra))
    print()
    data = parse(lines)
    extra = process(data)
    print('sol 2:', solve_2(data, extra))