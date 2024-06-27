# contains functions to determine distances
# Mahir Tuzcu - 11070978

import numpy as np
import math

def dynamic_list(item, key, list):
    if list == None:
        list = [[], [], -1]
    if len(list[0]) > 0:
        last = list[1][list[2]]
    if len(list[0]) == 0 or key > last:
        list[0].insert(list[2], item)
        list[1].insert(list[2], key)
        list[2] = -1
    else:
        list[0].insert(list[2], item)
        list[1].insert(list[2], key)
        list[2] += -1
    return list

def cord_filter(input_object) -> tuple:
    """takes a tuple or object and returns (x, y) coordinates if input is an object
    or returns input if input was already a (x, y) tuple"""
    if isinstance(input_object, tuple):
        return input_object
    else:
        return input_object.cords
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
    distance = (abs(cords1[0] - cords2[0]) + abs(cords1[1] - cords2[1]))
    return distance

def get_neighbours(cords, size):
    """returns list of neighbouring (x, y) coordinate in tuple form if they are within bounds"""
    neighbours = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_x, next_y = cords[0] + dx, cords[1] + dy
        if 0 <= next_x < size and 0 <= next_y < size:
            neighbours.append((next_x, next_y))
    return neighbours

def get_distances(node0, id):
    """returns the distances between node0 and all nodes of type (id = 1; house), (id = 2; battery)"""
    if id == 1:
        node_list = node0.grid.houses
    if id == 2:
        node_list = node0.grid.batteries
    distances = None
    for node1 in node_list:
        if node1 != node0:
            key = manhatten_distance(node0, node1)
            distances = dynamic_list(node1, key, distances)
    return distances[0]

def get_cable_distances(grid):
    new_list = None
    for house in grid.houses:
        key = house.distance
        new_list = dynamic_list(house, key, new_list)
    grid.houses = new_list[0]



    



