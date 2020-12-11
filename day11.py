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

INPUT = 'day11_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    out = [] 
    for l in lines:
        l = l.strip()
        out.append(list(l))
    return out 
# parse = parse_by_blank

# def solve_1(data):
#     data = set(data)
#     device = max(data) + 3
    
#     paths = [(device, )]
#     while paths:
#         print(paths)
#         path = paths.pop() 
#         tail = path[-1]

#         if tail == 0: return path

#         for i in range(3):
#             if tail - i in data - set(path):
#                 paths.append(path + (tail - i, ))

#     return paths

SHIFTS = [(-1)]

OCCUPIED = "#"
EMPTY = 'L'
FLOOR = '.'

def count_adjacent(seats, r, c):
    x = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0: continue
            for mul in count():
                r2 = r+dr*mul
                c2 = c+dc*mul
                if not (0 <= r2 < len(seats) and 0 <= c2< len(seats[0])): break
                if seats[r2][c2] == OCCUPIED:
                    x += 1
                    break
    return x

from copy import deepcopy

def solve_1(data): 
    return
    # print(data)

    prev = data
    changed = True
    while changed:
        changed = False

        new_state = deepcopy(prev)
        for r in range(len(new_state)):
            for c in range(len(new_state[0])):
                old = prev[r][c]
                if old == FLOOR: continue
                if old == EMPTY:
                    if count_adjacent(prev, r, c) == 0:
                        new = OCCUPIED
                    else:
                        new = EMPTY
                elif old == OCCUPIED:
                    if count_adjacent(prev, r, c) >= 4:
                        new = EMPTY
                    else:
                        new = OCCUPIED
                if new != old: changed = True
                new_state[r][c] = new

        prev = new_state

    return sum(sum(x == OCCUPIED for x in row) for row in new_state)

from sortedcontainers import sorteddict, sortedlist

def solve_2(data):
    


    row_seats = defaultdict(sortedlist.SortedList)
    col_seats = defaultdict(sortedlist.SortedList)
    dd_seats = defaultdict(sortedlist.SortedList)
    du_seats = defaultdict(sortedlist.SortedList)

    def adj(r, c):
        dd = r + c
        du = r - c

        x = 0
        if row_seats[r]:
            x += row_seats[r][0] < c
            x += row_seats[r][-1] > c
        if col_seats[c]:
            x += col_seats[c][0] < r
            x += col_seats[c][-1] > r
        if du_seats[du]:
            x += du_seats[du][0] < dd
            x += du_seats[du][-1] > dd
        if dd_seats[dd]:
            x += dd_seats[dd][0] < du
            x += dd_seats[dd][-1] > du
        return x

    while True:
        a, b, c2, d = row_seats, col_seats, dd_seats, du_seats

        new_occupied = []
        new_empty = []

        for r in range(len(data)):
            for c in range(len(data[0])):
                if data[r][c] == FLOOR: continue
                occ = c in row_seats[r]
                old = OCCUPIED if occ else EMPTY

                if old == EMPTY:
                    if adj(r, c) == 0:
                        new = OCCUPIED
                    else:
                        new = EMPTY
                else:
                    if adj( r, c) >= 5:
                        new = EMPTY
                    else:
                        new = OCCUPIED

                if new != old: 
                    if new == OCCUPIED:
                        new_occupied.append((r, c))
                    else:
                        new_empty.append((r, c))
        print(new_occupied)
        print(new_empty)
        for r, c in new_empty:
            dd = r + c
            du = r - c
            a[r].remove(c)
            b[c].remove(r)
            c2[dd].remove(du)
            d[du].remove(dd)

        for r, c in new_occupied:
            dd = r + c
            du = r - c
            a[r].add(c)
            b[c].add(r)
            c2[dd].add(du)
            d[du].add(dd)

        print('---')
        for row in row_seats.values():
            x = [' ']*len(data[0])
            for i in row:
                x[i] = '#'
            print(''.join(x))

        if not new_occupied and not new_empty:
            break

    print(row_seats)
    print(col_seats)
    print(dd_seats)
    print(du_seats)

    x = 0
    for row in row_seats.values():
        x += len(row)

    print(sum(len(y) for y in col_seats.values()    ))
    print(sum(len(y) for y in dd_seats.values()    ))
    print(sum(len(y) for y in du_seats.values()    ))

    return x


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))