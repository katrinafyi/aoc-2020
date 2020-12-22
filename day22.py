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

INPUT = 'day22_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    p1, p2 = parse_by_blank(lines) 
    p1 = deque(lmap(int, p1[1:]))
    p2 = deque(lmap(int, p2[1:]))
    return p1, p2

def solve_1(data):
    data = lmap(deque, data)
    p1, p2 = data
    while p1 and p2:
        # print(p1)
        # print(p2)
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            x = p1
        else:
            x = p2
        x.extend(sorted((c1, c2))[::-1])

    x = p1 or p2
    print(x)
    y = 0
    for i, c in enumerate(reversed(x)):
        y += (i+1) * c
    return y

def recursive(p1, p2):
    assert p1 or p2

    prev = set()
    while p1 and p2:

        p = (tuple(p1), tuple(p2))
        if p in prev:
            return 0
        prev.add(p)

        c1 = p1.popleft()
        c2 = p2.popleft()

        if len(p1) >= c1 and len(p2) >= c2: 
            p1x = deque(p1[i] for i in range(c1))
            p2x = deque(p2[i] for i in range(c2))
            w = recursive(p1x, p2x)
        else:
            w = 0 if c1 > c2 else 1

        pw = (p1, p2)[w]
        cw = (c1, c2)[w]
        cl = (c1, c2)[1-w]
        pw.append(cw)
        pw.append(cl)

    return 0 if p1 else 1


def solve_2(data):
    p1, p2 = data
    w = recursive(p1, p2)
    print(p1)
    print(p2)
    print(w)

    y = 0
    for i, c in enumerate(reversed((p1, p2)[w])):
        y += (i+1) * c
    return y
    

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        print('sol 2:', solve_2(data))