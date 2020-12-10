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

INPUT = 'day10_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    out = [] 
    for l in lines:
        l = l.strip()
        l = int(l)
        out.append(l)
    return out 
# parse = parse_by_blank

# def solve_1(data):
#     data = set(data)
#     device = max(data) + 3
    
#     paths = [(device, )]
#     while paths:
#         print(paths)
#         path = paths.pop() 
#         tail = path[-1]

#         if tail == 0: return path

#         for i in range(3):
#             if tail - i in data - set(path):
#                 paths.append(path + (tail - i, ))

#     return paths

def solve_1(data):
    data.append(0)
    data.append(max(data) + 3)
    
    data.sort()

    ones = 0
    three = 0
    for i in range(len(data) - 1):
        if data[i+1] - data[i] == 1: 
            ones += 1
        elif data[i+1] - data[i] == 3:
            three += 1

    return ones * three

from functools import lru_cache

@lru_cache(maxsize=None)
def solve(data, prev, i):
    if i == len(data): return 1
    if data[i] - prev > 3: return 0
    x = solve(data, data[i], i+1)
    # print(' '*i, 'include', data[i])
    if i+1 < len(data) and data[i+1] - prev <= 3:
        # print(' '*i,  'exclude', data[i])
        x += solve(data, prev, i+1)
    return x

def solve_2(data):
    data.sort()
    return solve(tuple(data), 0, 0)

    table = [None] * len(data)
    table[-1] = 1

    for i in reversed(range(len(data) - 1)):
        if data[i+1] - data[i] <= 3:
            table[i] = 2*table[i+1]
        else:
            table[i] = table[i+1]
    print(table)
    return table[0]


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        # print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))