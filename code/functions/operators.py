# contains functions to determine distances
# Mahir Tuzcu - 11070978

import functions
import random as rand
import classes
import os
import sys
import algorithms
from pathlib import Path

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
      
def intermediate_result(steps, cost, itterations):
    print(f"{steps}, {cost}, {itterations}") 

# these functions check if the given arguments are valid
def process_input(argv):
        
    if len(argv) not in (3, 4): 
        print(f"ERROR: wrong arguments. usage script.py <disctrict_file> <algorithm(random, hillcimber, annealing)> <itterations (set 0 or leave empty for no itteration limit)>") 
        sys.exit(2) 
        
    district_path = Path("../districts") / argv[1]
    if os.path.isdir(district_path) == False:
        print(f"ERROR: district file does not exist") 
        sys.exit(3)
    
    if argv[2] == 'random':
        algorithm = algorithms.random()
    elif argv[2] == 'hillclimber':
        algorithm = algorithms.hillclimber()
    elif argv[2] == 'annealing':
        algorithm = algorithms.annealing()
    else:
        print(f"ERROR: first argument has to be (random, hillcimber, annealing)") 
        sys.exit(2)
    
    # check if itteration limit is provided
    if len(argv) == 4:
        try:
            itteration_limit = int(argv[3])  
            if itteration_limit < 0: 
                raise ValueError
        except ValueError:
            print("Error: Fourth argument (itteration limit) must be a empty, a positive integer or 0")
            sys.exit(3)  
    else:
        itteration_limit = 0

    # create grid 
    grid = classes.Grid()
    grid.create_grid(district_path)  

    # return the proper variables
    return grid, algorithm, itteration_limit