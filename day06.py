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

INPUT = 'day06_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    lines = ''.join(lines).split('\n\n')

    return lines

def solve_1(data):

    x = 0
    for group in data:
        q = set()
        group = group.split('\n')
        for person in group:
            q.update(person)
        x+= len(q)

    return x

def solve_2(data):
    
    x = 0
    for group in data:
        group = group.split('\n')
        q = set(group[0])
        for person in group[1:]:
            q &= set(person)
        x+= len(q)

    return x

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))