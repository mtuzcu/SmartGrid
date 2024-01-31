# contains functions to determine distances
# Mahir Tuzcu - 11070978

import numpy as np
import math

def cord_filter(input_object) -> tuple:
    """takes a tuple or object and returns (x, y) coordinates if input is an object
    or returns input if input was already a (x, y) tuple"""
    if isinstance(input_object, object):
        return input_object.get_cords()
    if isinstance(input_object, tuple):
        return input_object
    print("ERROR: No coordinates detected")
    return (0,0)

def euclidean_distance(node1, node2) -> float:
    """returns the distance between node1 and node2. Input can either be an object or
    the (x, y) coordinates in tuple format of the object"""
    cords1 = cord_filter(node1)
    cords2 = cord_filter(node2)
    return ((cords1[0] - cords2[0]) ** 2 + (cords1[1] - cords2[1]) ** 2) ** 0.5

def manhatten_distance(node1, node2) -> int:
    """returns manhatten distance between node1 and node2. Input can either be an object or
    the (x, y) coordinates in tuple format of the object"""
    cords1 = cord_filter(node1)
    cords2 = cord_filter(node2)
    return (math.abs(cords1[0] - cords2[0]) + math.abs(cords1[1] - cords2[1]))

def get_neighbours(x, y, size):
    """returns list of neighbouring (x, y) coordinate in tuple form if they are within bounds"""
    neighbours = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_x, next_y = x + dx, y + dy
        if 0 <= next_x <= size and 0 <= next_y <= size:
            neighbours.append(x + dx, y + dy)
    return neighbours


