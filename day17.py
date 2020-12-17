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

INPUT = 'day17_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

ACTIVE = '#'
INACTIVE = '.'

def parse(lines: List[str]):
    out = {}
    for y, row in enumerate(lines):
        for x, c in enumerate(row.strip()):
            out[x, y, 0] = c == ACTIVE
    return out
    

from itertools import product

def solve_1(data):
    # active = {k for k, v in data.items() if v}
    # print(active)

    def adj(pos):
        x,y,z=pos
        for dx, dy, dz in product((1, 0, -1), repeat=3):
            if dx == dy == dz == 0: continue 
            yield x+dx,y+dy,z+dz
    active = defaultdict(bool, data)

    num_adjacent = defaultdict(int)
    for pos, s in (active.items()):
        for a in adj(pos):
            num_adjacent[a] += s
    
    active = {k for k, v in data.items() if v}

    def dump():
        for z in range(-2, 3):
            print('z', z)
            for y in range(-3, 4):
                for x in range(-3, 4):
                    print('#' if (x,y,z) in active else '.', end='')
                print()
            print()

    for i in range(6):
        # print(active)
        # print('-'*20)
        # dump()
        new_active = []
        new_inactive = []

        for pos, num in num_adjacent.items():
            old = pos in active
            new = old
            if old:
                if 2<=num<=3:
                    pass
                else:
                    new = False
            else:
                if num == 3:
                    new = True

            if new != old:
                if new:
                    new_active.append(pos)
                else:
                    new_inactive.append(pos)

        for pos in new_active:
            for a in adj(pos):
                num_adjacent[a] += 1
            # assert act not in active
            active.add(pos)

        for pos in new_inactive:
            for a in adj(pos):
                num_adjacent[a] -= 1
                # assert num_adjacent[a] >= 0
            # assert act in active
            active.remove(pos)
        # print(min(num_adjacent.values()))
        # print('active', new_active)
        # print('inactive', new_inactive)
        # input()

    return len(active)

def solve_2(data):
    # active = {k for k, v in data.items() if v}
    # print(active)

    data = {k + (0, ): v for k, v in data.items()}

    def adj(pos):
        x,y,z, a=pos
        for dx, dy, dz, da in product((1, 0, -1), repeat=4):
            if dx == dy == dz ==da== 0: continue 
            yield x+dx,y+dy,z+dz,a+da

    active = defaultdict(bool, data)

    num_adjacent = defaultdict(int)
    for pos, s in (active.items()):
        for a in adj(pos):
            num_adjacent[a] += s
    
    active = {k for k, v in data.items() if v}

    def dump():
        for z in range(-2, 3):
            print('z', z)
            for y in range(-3, 4):
                for x in range(-3, 4):
                    print('#' if (x,y,z) in active else '.', end='')
                print()
            print()

    for i in range(6):
        # print(active)
        # print('-'*20)
        # dump()
        new_active = []
        new_inactive = []

        for pos, num in num_adjacent.items():
            old = pos in active
            new = old
            if old:
                if 2<=num<=3:
                    pass
                else:
                    new = False
            else:
                if num == 3:
                    new = True

            if new != old:
                if new:
                    new_active.append(pos)
                else:
                    new_inactive.append(pos)

        for pos in new_active:
            for a in adj(pos):
                num_adjacent[a] += 1
            # assert act not in active
            active.add(pos)

        for pos in new_inactive:
            for a in adj(pos):
                num_adjacent[a] -= 1
                # assert num_adjacent[a] >= 0
            # assert act in active
            active.remove(pos)
        # print(min(num_adjacent.values()))
        # print('active', new_active)
        # print('inactive', new_inactive)
        # input()

    return len(active)

if __name__ == "__main__":
    f = open(INPUT) if INPUT != 'in' else sys.stdin
    data = parse(f.readlines())
    print('sol 1:', solve_1(data))
    print()
    print('sol 2:', solve_2(data))