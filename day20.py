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

ROTATE = 100
FLIP_ROWS = 101
FLIP_COLS = 102

@dataclass(unsafe_hash=True)
class EdgeData:
    id: int
    top: str = None
    bottom: str = None
    left: str = None
    right: str = None
    ops: list = None

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
        e.ops = []

        return e 

    def rotate(self, n=1):
        # counter-clockwise
        e = self
        e.top, e.left, e.bottom, e.right = e.right, e.top[::-1], e.left, e.bottom[::-1]
        e.ops.append(ROTATE)
        if n > 1:
            self.rotate(n-1)
    
    def flip_rows(self):
        self.left = self.left[::-1]
        self.right = self.right[::-1]
        self.top, self.bottom = self.bottom, self.top
        self.ops.append(FLIP_ROWS)

    def flip_cols(self):
        self.top = self.top[::-1]
        self.bottom = self.bottom[::-1]
        self.left, self.right = self.right, self.left
        self.ops.append(FLIP_COLS)

    def transpose(self):
        self.left, self.top = self.top, self.left 
        self.right, self.bottom = self.bottom, self.right

    def copy(self):
        e = self
        return EdgeData(e.id, e.top, e.bottom, e.left, e.right, list(e.ops))

    def permutations(self):
        for i in range(4):
            yield self
            self.rotate()
        self.ops = self.ops[:-4]
        self.flip_rows()
        for i in range(4):
            yield self
            self.rotate()
        self.ops = self.ops[:-4]
        self.flip_cols()
        for i in range(4):
            yield self
            self.rotate()
        self.ops = self.ops[:-4]
        self.flip_rows()
        for i in range(4):
            yield self
            self.rotate()
        self.ops = self.ops[:-4]
        # self.transpose()
        # for i in range(4):
        #     yield self
        #     self.rotate()

    def apply(self, data):
        for op in self.ops:
            if op == FLIP_ROWS:
                data = data[::-1]
            elif op == FLIP_COLS:
                data = [x[::-1] for x in data]
            elif op == ROTATE:
                data = [''.join(x) for x in reversed(list(zip(*data)))]
        return data


def solve_1(data):
    # print(data)
    tiles = data

    num_tiles = len(tiles)

    t = next(iter(tiles.values()))
    tile_rows = len(t)
    tile_cols = len(t[0])

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
    from random import choice
    # tile_map[origin] = edges[choice(list(edges.keys()))]
    tile_map[origin] = edges.get(3187) or edges.get(1427)

    used = { tile_map[origin].id }
    q = deque([(origin, tile_map, used)])
    solutions = []
    while q:
        pos, tile_map, used = q.pop()
        this_perm = tile_map[pos]
        # print(pos)
        # print(len(tile_map))

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
            # if len(tile_map) < num_tiles:
            #     q.append((adj, tile_map, used))

        if not continuing and len(tile_map) == num_tiles:
            solutions.append(tile_map)
            break

    for tile_map in solutions:
        min_x  = min(x[0] for x in tile_map)
        max_x  = max(x[0] for x in tile_map)
        min_y  = min(x[1] for x in tile_map)
        max_y  = max(x[1] for x in tile_map)
        xs = max_x - min_x + 1
        ys = max_y - min_y + 1
        #     # print('non square', len(tile_map))
        # if xs * ys != 9 or len(tile_map) != 9: continue
        print()
        for y in range(min_y, max_y + 1):
            print([tile_map[x,y].id if (x,y) in tile_map else None 
                for x in range(min_x, max_x + 1)])

        edge_len = len(td.top)
        blank = ' ' * edge_len
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print(tile_map[x,y].top if (x,y) in tile_map else blank, end=' ')
            print()
            for i in range(1, edge_len - 1):
                for x in range(min_x, max_x + 1):
                    data = tile_map.get((x,y))
                    if not data: 
                        l = r = ' '
                    else: 
                        l = data.left[i]
                        r = data.right[i]
                    if i == 1 and data:
                        print(l + str(data.id).center(edge_len - 2) + r, end=' ')
                    else:
                        print(l + ' ' * (edge_len - 2) + r, end=' ')
                print()
            for x in range(min_x, max_x + 1):
                print(tile_map[x,y].bottom if (x,y) in tile_map else blank, end=' ')
            print()
            print()

    min_x  = min(x[0] for x in tile_map)
    max_x  = max(x[0] for x in tile_map)
    min_y  = min(x[1] for x in tile_map)
    max_y  = max(x[1] for x in tile_map)
    xs = max_x - min_x + 1
    ys = max_y - min_y + 1

    tile_images = {}
    for pos, data in tile_map.items():
        # print(pos, data.ops)
        im = data.apply(tiles[data.id])
        im = im[1:-1]
        im = [x[1:-1] for x in im]
        tile_images[pos[0] - min_x, pos[1] - min_y] = im

    image_dim = tile_rows - 2

    image = []
    for y in range(ys):
        rows = ['' for _ in range(image_dim)]
        for x in range(xs):
            for r in range(image_dim):
                rows[r] += (tile_images[x,y][r])
        image.extend(rows)
    print(image)
    '''
                1111111111
      01234567890123456789
    0                   # 
    1 #    ##    ##    ###
    2  #  #  #  #  #  #   
    '''
    monster = [(0, 18), (1, 0), (1, 5), (1, 6), (1, 11), (1, 12), (1, 17), (1, 18), (1, 19), (2, 1), (2, 4), (2, 7), (2, 10), (2, 13), (2, 16)]
    def monster_at(r,c):
        matches = set()
        try:
            for dr, dc in monster:
                if image[r+dr][c+dc] == '#':
                    matches.add((r+dr, c+dc))
        except IndexError:
            matches = ()
        if len(matches) == len(monster):
            print(matches)
            return matches 
        else:
            return set()

    original = image
    for perm in tile_map[origin].permutations():
        image = perm.apply(original)
        
        monster_pos = set()
        for r in range(len(image)):
            for c in range(len(image[0])):
                monster_pos |= monster_at(r, c)

        if monster_pos: 
            break

    return sum(x.count('#') for x in image) - len(monster_pos)

    # image = [[] for _ in 

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