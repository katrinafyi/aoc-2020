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

INPUT = 'day07_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    bags = {}
    for line in lines:
        line = line.strip('\n.').replace('bags', 'bag').replace(' bag', '')
        bag, contents = line.split(' contain ')
        contents = contents.split(', ')
        inner_bags = {}
        if 'no other' in contents:
            contents = []
        else:
            for content in tuple(contents):
                num, colour = content.split(' ', 1)
                inner_bags[colour] = num
        bags[bag] = inner_bags
    return bags
# parse = parse_by_blank

def solve_1(data):
    reverse_map = defaultdict(set)
    for colour, inner in data.items():
        for in_colour, in_num in inner.items():
            reverse_map[in_colour].add(colour)

    s = set()
    q = ['shiny gold']
    while q:
        x = q.pop()
        if x in s:
            continue 
        s.add(x)
        for y in reverse_map[x]:
            q.append(y)
    s.discard('shiny gold')
    print(s)
    return len(s)
    


def num_contains(bags, bag):
    return 1 + sum(int(num) * num_contains(bags, bag) for bag, num in bags[bag].items())

def solve_2(data):
    return num_contains(data, 'shiny gold') - 1

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))