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

INPUT = 'day16_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    grouped = parse_by_blank(lines)
    rules = [] 
    for rule in grouped[0]:
        name = rule.split(':')[0]
        nums = uints(rule)
        rules.append((name, ((nums[0], nums[1]), (nums[2], nums[3]))))
    print(rules)

    ticket = ints(grouped[1][1])
    print(ticket)
    nearby = lmap(ints, grouped[2])
    print(nearby)

    return rules, ticket, nearby

def is_valid(ranges, num):
    return any(low <= num <= high for low, high in ranges)

def solve_1(data):
    rules, ticket, nearby = data 
    x = 0
    for ticket in nearby:
        for n in ticket:
            valid = False
            for name, rule in rules:
                valid |= is_valid(rule, n)
            if not valid: 
                x += n

    return x

def solve_2(data):
    rules, my_ticket, nearby = data 
    valid_tickets = []
    for ticket in nearby:
        if not ticket: continue
        ticket_valid = True
        for n in ticket:
            valid = False
            for name, rule in rules:
                valid |= is_valid(rule, n)
            ticket_valid &= valid
        if ticket_valid:
            valid_tickets.append(ticket)

    rules = {k: v for k, v in rules}

    field_names = set(rules)
    possible_fields = [set(field_names) for _ in my_ticket]
    print(possible_fields)

    while True:
        for ticket in valid_tickets:
            for i, val in enumerate(ticket):
                for name in tuple(possible_fields[i]):
                    if not is_valid(rules[name], val):
                        possible_fields[i].remove(name)
        
        locked = {}
        for i, possible in enumerate(possible_fields):
            assert len(possible) >= 1
            if len(possible) == 1:
                locked[next(iter(possible))] = i
        
        if len(locked) == len(my_ticket):
            break

        for l, v in locked.items():
            for i, p in enumerate(possible_fields):
                if i != v:
                    p.discard(l)

    print(possible_fields)

    x = 1 
    for p, n in zip(possible_fields, my_ticket):
        if next(iter(p)).startswith('departure'):
            x *= n
    return x

if __name__ == "__main__":
    f = open(INPUT) if INPUT != 'in' else sys.stdin
    data = parse(f.readlines())
    print('sol 1:', solve_1(data))
    print()
    print('sol 2:', solve_2(data))