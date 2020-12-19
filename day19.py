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

INPUT = 'day19_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse_rule(line):
    num, data = line.split(': ')
    num = int(num)
    if '"' in data:
        return num, data.strip('"')
    data = data.split(' | ')
    data = lmap(ints, data)
    return num, data

def parse(lines: List[str]):
    rules, data = parse_by_blank(lines)
    x = {}
    for r in rules:
        k, v = (parse_rule(r))
        x[k] = v
    return x, lmap(str.strip, data)

def count_satisfied(rules, texts):

    def satisfies(num, text):
        rule = rules[num]
        if isinstance(rule, str):
            return (1, ) if text and rule == text[0] else ()
        else:
            matches = []
            for alt in rule:
                # print('alt', alt)
                used = [0]
                for part in alt:
                    # print('part', part)
                    part_used = []
                    for u in used:
                        part_used.extend(u + x for x in satisfies(part, text[u:]))
                    # print('part_used', part_used)
                    used = part_used
                
                matches.extend(used)
            return matches

    # print(satisfies(0, 'aa'))

    x = 0 
    for t in texts:
        for sat in satisfies(0, t):
            if sat == len(t):
                x += 1
                break
    return x 


def solve_1(data):
    rules, data = data

    # rules = {
    #     0: ((2, ), (3, ), (2, 2)),
    #     2: 'a',
    #     3: 'b'
    # }

    return count_satisfied(rules, data)


def solve_2(data):

    rules, data = data
    
    rules[8] = ((42,), (42, 8))
    rules[11] = ([42, 31], [42, 11, 31])
    
    return count_satisfied(rules, data)

if __name__ == "__main__":
    f = open(INPUT) if INPUT != 'in' else sys.stdin
    data = parse(f.readlines())
    print('sol 1:', solve_1(data))
    print()
    print('sol 2:', solve_2(data))