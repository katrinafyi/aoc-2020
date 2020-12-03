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

INPUT = 'day03_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return lmap(str.strip, lines)

def solve_1(data):
    r = 0
    c = 0
    rows = len(data)
    cols = len(data[0])
    x = 0
    while r < rows:
        if data[r][c % cols] == '#': x += 1
        r += 1
        c += 3
    return x

def solve_2(data):
    
    slopes = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
    ]

    y = 1
    for dr, dc in slopes:
        r = 0
        c = 0
        rows = len(data)
        cols = len(data[0])
        x = 0
        while r < rows:
            if data[r][c % cols] == '#': x += 1
            r += dr
            c += dc
        y *= x
    return y

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))