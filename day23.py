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
    return deque(lmap(int, lines[0].strip()))

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

@dataclass
class Node:
    value: None = None
    next: None = None

    def insert_right(self, value):
        self.next = Node(value, self.next)
        return self.next

    def link_right(self, right):
        right.next = self.next
        self.next = right

    def unlink_right(self):
        right = self.next
        self.next = right.next
        
        right.next = None
        return right

    @classmethod
    def from_list(cls, items):
        head = cls()
        current = head
        for x in items:
            current = current.insert_right(x)
        head = head.next 
        return head, current

    def __repr__(self):
        x = []
        current = self
        while current.next:
            x.append(current.value)
            current = current.next
            if current is self: 
                x.append(...)
                break
        return repr(x)

    __str__ = __repr__

def solve_2(data, extra):
    cups = data
    low = min(cups)
    high = max(cups)
    million = 1000000

    print(cups)
    head, tail = Node.from_list(cups)
    for i in range(high + 1, million + 1):
        tail = tail.insert_right(i)
    print('list made')

    tail.next = head 

    num_to_node = [None]*(1+million)
    c = head
    while c is not None:
        num_to_node[c.value] = c
        c = c.next
        if c is head: break
    print(len(num_to_node))
    print(tail.value)
    print(head.value)
    print('dict made')

    cur = head
    limit = 10 * million
    for i in range(limit):
        # print(cur)
        if i % 100000 == 0: print(i / limit)
        #print(cups)
        # cur at current cup
        c = cur.value

        three = []
        for x in range(3):
            three.append(cur.unlink_right())
        three_vals = [x.value for x in three]

        target = c - 1
        while target < low or target in three_vals:
            target -= 1
            if target < low:
                target = high
        
        s = num_to_node[target]
        for x in reversed(three):
            s.link_right(x)

        cur = cur.next

    # print(cur)
    # print(cur)
    c = num_to_node[1]
    a, b = c.next.value, c.next.next.value
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