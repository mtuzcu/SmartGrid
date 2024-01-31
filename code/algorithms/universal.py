# contains universal algorithm script

from classes.grid import *
from functions.distance import *
from functions.Random import *
from functions.simulation import *
from algorithms.general import *

class algorithm_executor():

    def __init__(self, grid) -> None:
        self.itterations = 10000
        self.grid = grid

    def run_algorithm(self):
        
        for i in range(0, self.itterations):
            for house in self.grid.houses:
                battery = random_algorithm(self.grid, house)
                print(battery)
                print(house.get_cords, battery.get_cords)
                astar(battery, house)
          

            if district_solved(self.grid) == 0:
                print("succes!")
                break
