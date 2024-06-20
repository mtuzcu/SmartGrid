# Contains Functions involving random actions
# Mahir Tuzcu - 11070978

import random as rand
from classes.grid import *

def get_node(grid, node):
    if isinstance(node, tuple):
        node = grid[node]
    if isinstance(node, object):
        node = grid[node.cords]
    return node

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

def get_inverse_component(grid, component: object) -> object:
    """returns a new random component. If input component is house, returns a battery 
    and vice versa"""
    random_component = None
    if component.id == 0:
        random_component = get_random_component(grid.batteries)

    if component.id == 1:
        random_component = get_random_component(grid.houses)
    return random_component