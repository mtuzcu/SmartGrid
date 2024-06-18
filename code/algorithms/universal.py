# contains universal algorithm script

import random as ran
from classes.grid import *
import functions
from algorithms.general import *

class algorithm_executor():

    def __init__(self, grid) -> None:
        self.itterations = 100000
        self.grid = grid

    def run_algorithm(self):
        
        for i in range(0, self.itterations):
            random_algorithm(self.grid)
            #astar(self.grid, battery, house)
          
            #if functions.district_solved(self.grid) == 20:
                #print("succes!")
                #break
        print(self.grid.N_connected_houses)
