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

INPUT = 'day08_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    out = [] 
    for l in lines:
        l = l.strip()
        op, arg = l.split()
        arg = int(arg) 
        out.append((op, arg))
    return out 
# parse = parse_by_blank

def solve_1(data):
    i = 0
    acc = 0
    seen = set() 
    while i not in seen:
        seen.add(i)

        op, arg = data[i]
        if op == 'acc':
            acc += arg 
            i += 1
        elif op == 'nop':
            i += 1
        elif op == 'jmp':
            i += arg
        
    return acc


def test(data):
    i = 0
    acc = 0
    seen = set() 
    while i not in seen:
        seen.add(i)

        op, arg = data[i]
        if op == 'acc':
            acc += arg 
            i += 1
        elif op == 'nop':
            i += 1
        elif op == 'jmp':
            i += arg
        if i == len(data):
            return acc

    return None

def switch(op):
    return 'nop' if op == 'jmp' else 'jmp'

def solve_2(data):
    
    for i in range(len(data)):
        copy = list(data)
        op, arg = copy[i]
        if op not in ('nop', 'jmp'): continue
        copy[i] = (switch(op), arg)
        result = test(copy)
        if result is not None: return result

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))