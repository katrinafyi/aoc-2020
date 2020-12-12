# generously donated by max bo, with minor alterations

""" Coordinate system (ab)using the complex numbers of python.

Coordinate plane is in MATHEMATICAL convention (+j is up, +1 is right).
Angles are in MATHEMATICAL convention. +theta is rotation counter-clockwise.

to_/from_pos will convert to/from computer graphics convention.

"""

import cmath
from math import degrees, radians

ORIGIN = 0 + 0j
CARDINALS = SHIFTS = SIDES = N, S, E, W = 1j, -1j, 1, -1
DIAGONALS = NE, SE, SW, NW = (N + E), (S + E), (S + W), (N + W)

DIRECTIONS = CARDINALS + DIAGONALS

COORD_TO_LETTER = dict(zip(
    (N, S, E, W, NE, SE, SW, NW), 
    ('N', 'S', 'E', 'W', 'NE', 'SE', 'SW', 'NW')
))
LETTER_TO_COORD = {v: k for k, v in COORD_TO_LETTER.items()}

def adjacents(c): 
    return [ c + i for i in CARDINALS ]
def adjacents_8(c): 
    return [ c + i for i in DIRECTIONS ]
neighbours = adjacents 
neighbours_8 = adjacents_8
def turn_left(c): 
    return c * 1j
def turn_right(c): 
    return c * -1j
def turn_around(c): 
    return c * -1
def turn(c, deg):
    return c * from_angle(deg)

rotate_left = turn_left
rotate_right = turn_right 
rotate = turn

_sorted_cardinals = (E, N, W, S)
def to_angle(c):
    return round(degrees(cmath.phase(c)))
def from_angle(d):
    if d % 90 == 0:
        return _sorted_cardinals[(d // 90) % 4]
    return cmath.rect(1, radians(d))

def to_pos(c):
    return (c.real, -c.imag)
def from_pos(pos, snd=None):
    if snd is None:
        x, y = pos 
    else: 
        x, y = pos, snd

    return complex(x, -y)

def ell1_norm(c): 
    return abs(c.real) + abs(c.imag)
manhattan_norm = ell1_norm
def euclidean_norm(c):
    return abs(c)