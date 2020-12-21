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

INPUT = 'day21_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    o = [] 
    for l in lines:
        ing, allergens = l.strip().split(' (contains ')
        ing = set(ing.split())
        allergens = set(allergens.rstrip(')').split(', '))
        o.append((ing, allergens))
    return o

def solve_1(data):
    ALL_INGREDIENTS = set.union(*[i for i, a in data])
    # print(data)
    # print(ALL_INGREDIENTS)

    aller_to_ings = defaultdict(ALL_INGREDIENTS.copy)
    for ings, allers in data:
        for a in allers:
            aller_to_ings[a] &= ings

    no_aller = ALL_INGREDIENTS - set.union(*aller_to_ings.values())
    print(no_aller)

    x = 0 
    for ings, allers in data:
        x += len(ings & no_aller)
    return x

def solve_2(data):
    ALL_INGREDIENTS = set.union(*[i for i, a in data])
    # print(data)
    # print(ALL_INGREDIENTS)

    aller_to_ings = defaultdict(ALL_INGREDIENTS.copy)
    for ings, allers in data:
        for a in allers:
            aller_to_ings[a] &= ings

    while any(len(x) > 1 for x in aller_to_ings.values()):
        for a, ings in aller_to_ings.items():
            if len(ings) == 1:
                i = just(ings)
                for a2, ings2 in aller_to_ings.items():
                    if a2 != a:
                        ings2.discard(i)

    print(aller_to_ings)

    ings = [(a, ings) for a, ings in just_dict(aller_to_ings).items()]
    print(ings)
    ings.sort() 
    print(','.join(x[1] for x in ings))


if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))