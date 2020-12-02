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

INPUT = 'day01_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

# remark: avoid one-use generators
def parse(lines: List[str]):
    return [ints(line)[0] for line in lines]

def solve_1(data):
    nums = set()
    for x in data:
        if 2020 - x in nums:
            return x * (2020 - x)
        nums.add(x)


def solve_2(data):
    nums = set()
    for x in data:
        for y in data:
            if 2020 - y - x in nums:
                return x * (2020 - y - x) * y
            nums.add(y)
        nums.add(x)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))