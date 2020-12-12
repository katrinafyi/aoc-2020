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

INPUT = 'day12_input.txt' if len(sys.argv) == 1 else sys.argv[1]

import coords as co

# import numpy as np 
# import scipy as sp

def parse(lines):
    out = [] 
    for l in lines:
        l = l.strip()
        dir, num = l[0], l[1:]
        num = int(num)
        out.append((dir, num))
    return out 
# parse = parse_by_blank

def solve_1(data): 
    pos = co.ORIGIN
    dir = co.E
    for action, dist in data:
        if action in 'NESW':
            pos += co.direction_map[action] * dist
        elif action in 'LR':
            assert dist % 90 == 0
            for i in range(dist // 90):
                f = co.turn_left if action == 'L' else co.turn_right
                dir = f(dir)
        elif action == 'F':
            pos += dist * dir
        else:
            assert 0
    
    return (co.cityblock_distance(pos))


def solve_2(data): 
    waypoint = 10 + 1j
    pos = co.ORIGIN
    for action, dist in data:
        if action in 'NESW':
            waypoint += co.direction_map[action] * dist
        elif action in 'LR':
            assert dist % 90 == 0
            for i in range(dist // 90):
                f = co.turn_left if action == 'L' else co.turn_right
                waypoint = f(waypoint)
        elif action == 'F':
            pos += dist * waypoint
        else:
            assert 0
    
    return (co.cityblock_distance(pos))


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))