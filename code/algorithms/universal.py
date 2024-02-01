# contains universal algorithm script

import random as ran
from classes.grid import *
from functions.distance import *
from functions.Random import *
from functions.simulation import *
from algorithms.general import *

class algorithm_executor():

    def __init__(self, grid) -> None:
        self.itterations = 100000
        self.grid = grid

    def run_algorithm(self):
        
        for i in range(0, self.itterations):
            house = get_random_component(self.grid.houses)
            battery = random_algorithm(self.grid, house)
            astar(self.grid, battery, house)
          

            if district_solved(self.grid) == 0:
                print("succes!")
                break
        print(self.grid.N_connected_houses)
