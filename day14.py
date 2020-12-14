from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *


DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day14_input.txt' if len(sys.argv) == 1 else sys.argv[1]

import coords as co

MASK = 'mask'
MEM = 'mem'

def parse(lines):
    out = [] 
    for l in lines: 
        l = l.strip()
        t = MASK if l[:4] == MASK else MEM
        if t == MEM:
            addr, val = ints(l)
        else:
            addr = None
            val = l.split()[-1]
        out.append((t, addr, val))
    
    return out
# parse = parse_by_blank

def apply_mask(mask, val):
    # ones must be set
    ones = int(mask.replace('X', '0'), 2)
    val |= ones
    # zeros must be cleared
    zeros = int(mask.replace('X', '1'), 2)
    val &= zeros
    return val

def solve_1(data): 
    memory = defaultdict(int)
    mask = None
    for t, addr, val in data:
        if t == MASK:
            mask = val
        elif t == MEM:
            memory[addr] = apply_mask(mask, val)

    x = 0 
    for v in memory.values():
        if v: x += v
    return x

def apply_mask_2(mask, val):
    # ones must be set
    ones = int(mask.replace('X', '0'), 2)
    val |= ones
    xs = [i for i, x in enumerate(mask) if x == "X"]
    
    val = list(bin(val)[2:].rjust(36, '0'))
    for c in range(2**mask.count('X')):
        bi = (bin(c)[2:].rjust(len(xs), '0'))
        for i, b in zip(xs, bi):
            val[i] = b
        yield (''.join(val))

def solve_2(data): 
    # print(*(apply_mask_2('00000000000000000000000000000000X0XX', int('000000000000000000000000000000011010'  , 2))), sep='\n')

    memory = defaultdict(int)
    mask = None
    for t, addr, val in data:
        if t == MASK:
            mask = val
        elif t == MEM:
            for x in apply_mask_2(mask, addr):
                memory[x] = val

    x = 0 
    for v in memory.values():
        if v: x += v
    return x


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        print('sol 2:', solve_2(data))