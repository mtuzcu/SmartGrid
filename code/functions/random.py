# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978

import random as rand
from classes.grid import *

def random(start = 0, end = 1) -> float:
    """returns a random float between[start, end]"""
    random_float = random.randint(start, end)
    return random_float

def select_random_index(N_candidates: int) -> int:
    """takes a number of candidates to randomly choose between and returns an index i"""    
    random_number = random()
    cummulative_sum = 0
    sum_delta = 1.0 / N_candidates
    for i in range(0, N_candidates):
        cummulative_sum += sum_delta
        if random_number <= cummulative_sum:
            return i

def get_random_key(dictionairy: dict):
    return rand.choice(list(dictionairy.keys()))

def get_random_component(dictionairy):
    return dictionairy[get_random_key(dictionairy)][0]

def select_random_component(candidates_list) -> object:
    """returns a randomly chosen component from list of eligible components"""
    index = select_random_index(len(candidates_list))
    return candidates_list[index]

def get_inverse_component(grid, component: object) -> object:
    """returns a new random component. If input component is house, returns a battery 
    and vice versa"""
    random_component = None
    if isinstance(component, House):
        random_component = get_random_component(grid.batteries)

    if isinstance(component, Battery):
        random_component = get_random_component(grid.houses)
    
    return random_component