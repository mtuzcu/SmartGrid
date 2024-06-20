# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
import functions
import copy
import math
import random

class hillclimber():

    def __init__(self, grid) -> None:
        self.solution = grid

    # Generate initial solution
    def generate_initial_solution(self):
        self.houses = self.solution.houses
        self.batteries = self.solution.batteries
        for house in self.houses:
            battery = functions.get_random_component(self.batteries)
            while battery.capacity < house.capacity:  # Ensure battery has enough capacity
                battery = functions.get_random_component(self.batteries)
            self.solution.connect(house, battery)
        return self.solution

    # Generate neighbor solution
    def generate_neighbour(self):
        house = functions.get_random_component(self.neighbour.houses)
        if random.random() < 0.5:
            battery = functions.get_random_component(self.neighbour.batteries)
            while battery.capacity < house.capacity:
                battery = functions.get_random_component(self.neighbour.batteries)
            current_battery = house.destination
            self.neighbour.disconnect(house, current_battery)
            self.neighbour.connect(house, battery)
            house.state = 1

        else:
        # Connect house to another house
            house2 = functions.get_random_component(self.neighbour.houses)
            if house2 != house and house + house2 <= new_solution[another_house][-1].capacity:
                new_solution[house] = [house, another_house] + new_solution[another_house]
                new_solution[another_house][-1].capacity -= house.output
    
    def store_solution(self):
        for house in self.neighbour.houses:
            if house.state == 1:
                house1 = self.solution[house.cords]
                battery1 = self.solution[house.destination.cords]
                self.solution.disconnect(house1, house1.destination)
                self.solution.connect(house1, battery1)
                house.state = 0

    def simulated_annealing(self, iter, T0 = 10000, alpha = 0.99):
        self.solution = self.generate_initial_solution()
        self.neighbour = copy.deepcopy(self.solution)
        T = T0
        lowest_cost = 0

        for k in range(iter):
            self.generate_neighbour()
            delta_E = self.neighbour.total_cost_cables - self.solution.total_cost_cables
            if delta_E < 0 or random.random() < math.exp(-delta_E / T):
                self.store_solution()
            
            T = T * alpha  # Cool down temperature

            if lowest_cost == 0 or self.solution.total_cost_cables < lowest_cost:
                lowest_cost = self.solution.total_cost_cables
                print(lowest_cost)
            #if T < 1e-10:  # Avoid temperature getting too low
                #break

        
        return self.solution
      