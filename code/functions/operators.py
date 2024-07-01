# contains functions to determine distances
# Mahir Tuzcu - 11070978

import functions
import random as rand
import classes

def manhattan_distance(node1, node2) -> int:
    """returns manhatten distance between node1 and node2. Input can either be an object or
    the (x, y) coordinates in tuple format of the object"""
    cords1 = node1.cords
    cords2 = node2.cords
    distance = (abs(cords1[0] - cords2[0]) + abs(cords1[1] - cords2[1]))
    return distance

def random(start = 0, end = 1) -> float:
    """returns a random float between[start, end]"""
    random_float = rand.randint(start, end)
    return random_float

def select_random_index(N_candidates: int) -> int:
    """takes a number of candidates to randomly choose between and returns an index i"""    
    random_int = rand.randrange(0, N_candidates)
    return random_int

def get_random_component(candidates_list: list) -> object:
    """returns a randomly chosen component from list of eligible components"""
    index = select_random_index(len(candidates_list))
    return candidates_list[index]
      


