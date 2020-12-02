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

INPUT = 'day02_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    out = []
    for l in lines:
        out.append((uints(l), l.split()[1][0], l.split()[-1]))
    return out

def solve_1(data):
    s = 0
    for policy, c, word in data:
        lo, hi = policy
        if lo <= word.count(c) <= hi:
            s += 1

    return s

def solve_2(data):
    s = 0
    for policy, c, word in data:
        lo, hi = policy
        low_match = word[lo - 1] == c
        high_match =  word[hi - 1] == c
        if (low_match or high_match) and (low_match != high_match):
            s += 1

    return s

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        print('sol 2:', solve_2(data))