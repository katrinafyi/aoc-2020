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

INPUT = 'day20_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    groups = parse_by_blank(lines)
    tiles = {} 
    for group in groups:
        tile, *data = group
        tile = ints(tile)[0]
        tiles[tile] = lmap(str.strip, data)
    return tiles

def opp(s):
    if s[0] == 'l':
        return 'right'
    if s[0] == 'r':
        return 'left'
    if s[0] == 't':
        return 'bottom'
    if s[0] == 'b':
        return 'top'
    assert 0

@dataclass(unsafe_hash=True)
class EdgeData:
    id: int
    top: str = None
    bottom: str = None
    left: str = None
    right: str = None

    @classmethod 
    def from_tile(cls, id, tile):
        rows = len(tile)
        cols = len(tile[0])

        def get_edge(data, r, c, dr, dc):
            x = [] 
            while r < rows and c < cols:
                x.append(data[r][c])
                r += dr 
                c += dc
            return ''.join(x)

        e = cls(id)
        data = tile
        e.left = get_edge(data, 0, 0, 1, 0)
        e.right = get_edge(data, 0, cols - 1, 1, 0)
        e.top = get_edge(data, 0, 0, 0, 1)
        e.bottom = get_edge(data, rows - 1, 0, 0, 1)

        return e 

    def rotate(self, n=1):
        e = self
        e.top, e.left, e.bottom, e.right = e.right, e.top[::-1], e.left, e.bottom[::-1]
        if n > 1:
            self.rotate(n-1)
    
    def flip_rows(self):
        self.left = self.left[::-1]
        self.right = self.right[::-1]

    def flip_cols(self):
        self.top = self.top[::-1]
        self.bottom = self.bottom[::-1]

    def copy(self):
        e = self
        return EdgeData(e.id, e.top, e.bottom, e.left, e.right)

    def permutations(self):
        for i in range(4):
            yield self
            self.rotate()
        self.flip_rows()
        for i in range(4):
            yield self
            self.rotate()
        self.flip_cols()
        for i in range(4):
            yield self
            self.rotate()
        self.flip_rows()
        for i in range(4):
            yield self
            self.rotate()

    def match(self, other, self_edge):
        target = getattr(other, opp(self_edge))
        get_current = lambda x: getattr(x, self_edge)

        for perm in self.permutations():
            if get_current(perm) == target:
                return
        assert False, "no match"


def solve_1(data):
    # print(data)
    tiles = data

    t = next(iter(tiles.values()))
    rows = len(t)
    cols = len(t[0])

    edges: Dict[int, EdgeData] = {}
    for num, data in tiles.items():
        edges[num] = EdgeData.from_tile(num, data)

    edges_to_permutations: Dict[str, Tuple[str, List[EdgeData]]] = defaultdict(list)
    for num, e in edges.items():
        for perm in e.permutations():
            for side in ('top', 'left', 'bottom', 'right'):
                edges_to_permutations[getattr(perm, side)].append((side, perm.copy()))

    t, td = next(iter(edges.items()))

    # print(edges_to_permutations)
    tile_map = {} 
    origin = 0,0
    tile_map[origin] = td 
    
    used = { td.id }
    q = deque([(origin, tile_map, used)])
    solutions = []
    while q:
        pos, tile_map, used = q.popleft()
        this_perm = tile_map[pos]
        # print(pos)

        continuing = False
        for adj, this_side in zip(neighbours(pos), ['top', 'bottom', 'left', 'right']):
            if adj in tile_map: continue
            # print(this_side, getattr(this_data, this_side))
            this_side_pattern = getattr(this_perm, this_side)
            # if this_side == 'left' or this_side == 'right':
            #     this_side_pattern = this_side_pattern[::-1]
            possible = edges_to_permutations[this_side_pattern]
            # print(adj, this_side, possible)
            for side, perm in possible:
                if perm.id in used: continue
                # if (adj, perm.id) in banned: continue
                if side == opp(this_side):
                    continuing = True
                    new_map = tile_map.copy()
                    new_map[adj] = perm 
                    q.append((adj, new_map, used | {perm.id}))

        if not continuing and len(tile_map) == len(edges):
            min_x  = min(x[0] for x in tile_map)
            max_x  = max(x[0] for x in tile_map)
            min_y  = min(x[1] for x in tile_map)
            max_y  = max(x[1] for x in tile_map)
            xs = max_x - min_x + 1
            ys = max_y - min_y + 1
            if xs == ys and len(tile_map) == xs * ys:
                pass
            #     # print('non square', len(tile_map))
            print()
            for y in range(min_y, max_y + 1):
                print([tile_map[x,y].id if (x,y) in tile_map else None 
                    for x in range(min_x, max_x + 1)])

    # print(set(tile_map))
    # print(tile_map)
    x = 1
    return

    def single_tile(e1, e2):
        return len(edge_to_num[e1]) == 1 and len(edge_to_num[e1[::-1]]) == 1 \
            and len(edge_to_num[e2]) == 1 and len(edge_to_num[e2[::-1]]) == 1 

    s = set()
    for num, e in edges.items():
        if single_tile(e.top, e.left):
            s.add(num)
        if single_tile(e.top, e.right):
            s.add(num)
        if single_tile(e.bottom, e.left):
            s.add(num)
        if single_tile(e.bottom, e.left):
            s.add(num)

    print(s)

    return x

    vert = [v[0] for k, v in vertical_edges.items() if len(v) == 1]
    vert = set(vert)
    hori = [v[0] for k, v in horizontal_edges.items() if len(v) == 1]
    hori = set(hori)
    print(vert & hori)
    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        data = parse(f.readlines())
        print('sol 1:', solve_1(data))
        print()
        f.seek(0)
        print('sol 2:', solve_2(data))