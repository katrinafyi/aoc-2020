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

INPUT = 'day15_input.txt' if len(sys.argv) == 1 else sys.argv[1]

import coords as co

def parse(lines: List[str]):
    return ints(lines[0])

def solve_1(data):
    print(data)
    prev_spoke = defaultdict(list)
    for i, x in enumerate(data):
        prev_spoke[x].append(i)
    
    speak = data[-1]
    print(prev_spoke)

    for i in range(len(data), 2020):
        # print(i, 'prev', speak)
        prev = prev_spoke[speak]
        if len(prev) == 1:
            speak = 0
        else:
            speak = prev[-1] - prev[-2]
        # print(speak)
        prev_spoke[speak].append(i)
        
    return speak

def solve_2(data):
    print(data)
    prev_spoke = defaultdict(list)
    for i, x in enumerate(data):
        prev_spoke[x].append(i)
    
    speak = data[-1]
    print(prev_spoke)

    for i in range(len(data), 30000000):
        if i % 100000 == 0: print(i / 30000000)
        # print(i, 'prev', speak)
        prev = prev_spoke[speak]
        if len(prev) == 1:
            speak = 0
        else:
            speak = abs(prev[0] - prev[1])
        # print(speak)
        new_prev = prev_spoke[speak]
        if len(new_prev) < 2:
            new_prev.append(i)
        else:
            if new_prev[1] > new_prev[0]:
                new_prev[0] = i
            else:
                new_prev[1] = i
        
    return speak 

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        print('sol 2:', solve_2(data))