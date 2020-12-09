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

INPUT = 'day09_input.txt' if len(sys.argv) == 1 else sys.argv[1]

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

def solve_1(data):
    preamble = deque(data[:25])
    
    def test(num):
        for a, b in combinations(preamble, 2):
            if a + b == num:
                return True 
        return False

    for num in data[25:]:
        if not test(num):
            return num
        preamble.popleft()
        preamble.append(num)

def solve_2(data):
    target = solve_1(data)

    prefixes = [0]
    for num in data:
        prefixes.append(prefixes[-1] + num)

    for start in range(len(data) + 1):
        for end in range(len(data) + 1):
            if prefixes[end] - prefixes[start] == target:
                nums = data[start:end]
                a, b = min(nums), max(nums)
                print(start, end, a+b)

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))