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

INPUT = 'day13_input.txt' if len(sys.argv) == 1 else sys.argv[1]

import coords as co

# import numpy as np 
# import scipy as sp

def parse(lines):
    earliest = int(lines[0])
    bus_ids = [int(x)  if x != 'x' else None for x in lines[1].split(',')]
    
    return earliest, bus_ids
# parse = parse_by_blank

def solve_1(data): 
    # print(data)
    earliest, buses = data 
    wait = float('inf')
    bus = None
    for b in buses:
        if b is None: continue
        w = ceil(earliest / b) * b
        if w < wait:
            wait = w 
            bus = b

    return (wait - earliest) * bus

# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def solve_2(data): 
    earliest, buses = data 
    # print(data)
    ns = []
    a = []
    for i, b in enumerate(buses):
        if b == None: continue
        ns.append(b)
        a.append(-i)
    return chinese_remainder(ns, a)
    '''
    x mod data[0] == 0
    x mod data[1] == 1 
    x mod data[2] == 2
    ''' 
    return

def solve_2(data):
    _, buses = data  
    d = 1
    x = 1
    for i, b in enumerate(buses):
        if not b: continue
        while x % b != (-i) % b:
            x += d
        d = lcm(d, b)
    return (x)


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))