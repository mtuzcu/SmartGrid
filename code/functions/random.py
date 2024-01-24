# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978

from ..universal import *

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

def select_random_component(candidates_list) -> object:
    """returns a randomly chosen component from list of eligible components"""
    index = select_random_index(len(candidates_list))
    return candidates_list[index]

def get_random_component(component: object) -> object:
    """returns a new random component. If input component is house, returns a battery 
    and vice versa"""
    random_component = None
    if isinstance(component, House): 
        while random_component in (component, None):
            random_component, location = select_random_component(list(Grid.batteries.items()))

    if isinstance(component, Battery):
        while random_component in (component, None):
            random_component, location = select_random_component(list(Grid.houses.items()))
    
    return random_component