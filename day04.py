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

INPUT = 'day04_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

FIELDS = {
    'byr',
'iyr',
'eyr',
'hgt',
'hcl',
'ecl',
'pid',
'cid',
}

def parse_part(line):
    d = {}
    line = line.split()
    for x in line:
        field, value = x.split(':') 
        d[field] = value 
    return d

def parse(lines: List[str]):
    out = [] 
    passport = {}
    for line in lines:
        line = line.strip() 
        if not line:
            out.append(passport)
            passport = {}
        passport.update(parse_part(line))

    if passport:
        out.append(passport)
    return out

def solve_1(data):
    x = 0
    for passport in data:
        missing = FIELDS - set(passport.keys())
        if 'cid' in missing:
            missing.remove('cid')
        if not missing:
            x += 1

    return x

def valid(key, value):
    if key == 'byr':
        return 1920 <= int(value) <= 2002
    elif key == 'iyr':
        return 2010 <= int(value) <= 2020
    elif key == 'eyr':
        return 2020 <= int(value) <= 2030
    elif key == 'hgt':
        num, unit = value[:-2], value[-2:]
        if unit == 'cm':
            return 150 <= int(num) <= 193 
        elif unit == 'in':
            return 59 <= int(num) <= 76
        return False
    elif key == 'hcl':
        if value[0] != '#': return False 
        if len(value[1:]) != 6: return False 
        return set(value[1:]) <= set('abcdef1234567890')
    elif key == 'ecl':
        return value in {'amb' ,'blu' ,'brn' ,'gry' ,'grn' ,'hzl', 'oth'}
    elif key == 'pid':
        return len(value) == 9 and int(value) >= 0

def solve_2(data):
    x = 0
    for passport in data:
        missing = FIELDS - set(passport.keys())
        if 'cid' in missing:
            missing.remove('cid')
        if missing:
            continue
        is_valid = True
        for key, value in passport.items():
            if key == 'cid': continue
            if not valid(key, value): is_valid = False

        if is_valid:
            x += 1


    return x

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(list(f.readlines()))
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))