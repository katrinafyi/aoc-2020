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

INPUT = 'day05_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    out = [] 
    for l in lines:
        l = l.strip() 
        out.append(l)
    return out

def solve_1(data):
    m = 0
    for seat in data:
        first, second = seat[:7], seat[-3:]
        first = first.replace('F', '0').replace('B', '1')
        first = int(first, 2)
        second = second.replace('L', '0').replace('R', '1')
        second = int(second, 2)
        row = first 
        col = second

        m = max(m, row * 8 + col)
        
    return m

def solve_2(data):

    seen = set()

    for seat in data:
        first, second = seat[:7], seat[-3:]
        first = first.replace('F', '0').replace('B', '1')
        first = int(first, 2)
        second = second.replace('L', '0').replace('R', '1')
        second = int(second, 2)
        row = first 
        col = second


        id = row * 8 + col

        seen.add(id)

    return set(range(min(seen), max(seen))) - seen


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))