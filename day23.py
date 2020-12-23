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

INPUT = 'day23_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return deque(lmap(int, lines[0]))

def process(data):
    return

def solve_1(data, extra):
    cups = data
    low = min(cups)
    high = max(cups)
    for move in range(100):
        # if move % 1000 == 0: print(move / 1000000)
        #print(cups)
        current = cups.popleft()
        cups.append(current)
        #print('c', current)
        three = [cups.popleft() for x in 'aaa']
        next_current = cups[0]
        #print(three)
        target = current - 1
        while target < low or target in three:
            target -= 1
            if target < low:
                target = high
        #print(target)
        while cups[0] != target:
            cups.append(cups.popleft())

        # current to end
        t = cups.popleft() 
        for x in three[::-1]:
            cups.appendleft(x)
        cups.appendleft(t)
    
        while cups[0] != next_current:
            cups.append(cups.popleft())

    #print(cups)
    print(cups)


def solve_2(data, extra):
    cups = data
    low = min(cups)
    high = max(cups)
    old_high = high
    i = high + 1
    million = 1000000

    extra = million - len(cups)
    while len(cups) < million:
        cups.append(i)
        i += 1

    high = max(cups)
    move = 0
    while move < 10*million:
        print(move)
        while cups[0] - 1 == cups[-1]:
            a = cups.popleft() 
            b = cups.pop() 
            cups.append(a)
            cups.appendleft(b)
            move += 1

        #print(cups)
        current = cups.popleft()
        cups.append(current)
        #print('c', current)
        three = [cups.popleft() for x in 'aaa']
        next_current = cups[0]
        #print(three)
        target = current - 1
        while target < low or target in three:
            target -= 1
            if target < low:
                target = high
        #print(target)
        while cups[0] != target:
            cups.append(cups.popleft())

        # current to end
        t = cups.popleft() 
        for x in three[::-1]:
            cups.appendleft(x)
        cups.appendleft(t)
    
        while cups[0] != next_current:
            cups.appendleft(cups.pop())

        move += 1 


    #print(cups)
    i = cups.index(1)
    a, b = cups[i+1], cups[i+2]
    print(a, b)
    print(a*b)

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