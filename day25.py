from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import *
from itertools import *

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day25_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse_line(line):
    return line


def parse(lines: List[str]):
    lines = lmap(str.strip,lines)
    o = [] 
    for l in lines:
        o.append(int(l))
    return o

def process(data):
    return

# @lru_cache(maxsize=None)
def transform(subject, loop):
    return pow(subject, loop, 20201227)
    if loop > 0:
        return (transform(subject, loop-1) * subject) % 20201227
    return subject

def solve_loop(subject, target):
    x = 1 
    i = 0
    while x != target:
        x = (x * subject) % 20201227
        i += 1
    return i

def solve_1(data, extra):
    print(data)

    card_public, door_public = data

    m = 10000000
    # sys.setrecursionlimit(m + 100)
    card_loop = solve_loop(7, card_public)
    door_loop = solve_loop(7, door_public)

    enc_key = transform(door_public, card_loop)
    enc_key2 = transform(card_public, door_loop)

    print(enc_key, enc_key2)


def solve_2(data, extra):
    return

if __name__ == "__main__":
    with open(INPUT) as f:
        lines = f.readlines()
    data = parse(lines)
    extra = process(data)
    print('sol 1:', solve_1(data, extra))
    print()
    data = parse(lines)
    extra = process(data)
    print('sol 2:', solve_2(data, extra))