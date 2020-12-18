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

INPUT = 'day18_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    o = [] 
    for l in lines:
        l = l.strip() 
        o.append(l)
    return o

import ast

class SubtractToMultiply(ast.NodeTransformer):
    def visit_BinOp(self, node: ast.BinOp) -> Any:
        self.generic_visit(node)
        if isinstance(node.op, ast.Sub):
            return ast.BinOp(left=(node.left), op=ast.Mult(), right=(node.right))
        return node

def solve_1(data):
    x = 0
    for l in data:
        tree = ast.parse(l.replace('*', '-'), mode='eval')
        new = ast.fix_missing_locations(SubtractToMultiply().visit(tree))
        # print(ast.dump(new))
        x += eval(compile(new, 'x', 'eval'))
    return x

def eval_line(line):
    line = '(' + line + ')'
    line = line.replace('(', ' ( ').replace(')', ' ) ').split()
    line = [x for x in line if x]

    def eval_op(op, x, y):
        if op == '+': return x + y 
        elif op == '*': return x * y

    ops = []
    stack = []
    for c in line:
        # print(c, stack, ops)
        if c.isnumeric():
            c = int(c)
            stack.append(c)

            while stack[-2] is not None:
                x = stack.pop()
                op = ops.pop() 
                y = stack.pop()
                stack.append(eval_op(op, x, y))
                
        elif c == '(':
            stack.append(None)
        elif c == '+':
            ops.append(c)
        elif c == '*':
            ops.append(c)
        elif c == ')':
            while stack[-2] is not None:
                x = stack.pop()
                op = ops.pop() 
                y = stack.pop()
                stack.append(eval_op(op, x, y))
            num = stack.pop()
            stack.pop() 
            stack.append(num)

    assert len(stack) == 1

    return stack[0]


def solve_1(data):
    # eval_line(data[1])
    return sum(eval_line(l) for l in data)

def solve_1(data):
    import re 
    class N(int):
        def __sub__(self, o):
            return N(int(self) * int(o))
        def __add__(self, o):
            return N(int(self) + int(o))

    x = 0 
    for l in data:
        l = re.sub(r'(\d+)', r'N(\1)', l).replace(' * ', ' - ')
        # print(l)
        x += (eval(l))
        # break
    return x
    # eval_line(data[1])
        

def solve_2(data):
    import re 
    class N(int):
        def __sub__(self, o):
            return N(int(self) * int(o))
        def __truediv__(self, o):
            return N(int(self) + int(o))

    x = 0 
    for l in data:
        l = re.sub(r'(\d+)', r'N(\1)', l).replace(' + ', ' / ').replace(' * ', ' - ')
        # print(l)
        x += (eval(l))
        # break
    return x

if __name__ == "__main__":
    f = open(INPUT) if INPUT != 'in' else sys.stdin
    data = parse(f.readlines())
    print('sol 1:', solve_1(data))
    print()
    print('sol 2:', solve_2(data))