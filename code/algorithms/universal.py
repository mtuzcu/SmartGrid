# contains universal algorithm script

import random as ran
from classes.grid import *
import functions
from algorithms.general import *
import copy

class algorithm_executor():

    def __init__(self, grid) -> None:
        self.itterations = 10000000
        self.grid = grid
        self.best_grid = None

    def run_algorithm(self):
        
        lowest_cost = 0
        for i in range(0, self.itterations):
            random_algorithm(self.grid)
            #astar(self.grid, battery, house)

            if len(self.grid.cables) == 150:
                if lowest_cost == 0 or self.grid.total_cable_cost < lowest_cost:
                    del self.best_grid 
                    self.best_grid = copy.deepcopy(self.grid)
                    lowest_cost = self.grid.total_cable_cost
                    print(lowest_cost)
          
            #if functions.district_solved(self.grid) == 20:
                #print("succes!")
                #break
        print(len(self.best_grid.cables))
        return self.best_grid
