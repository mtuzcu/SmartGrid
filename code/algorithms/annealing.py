# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
import functions
import copy
import math
import random

class annealing():

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
    def generate_neighbour(self, T):
        house = functions.get_random_component(self.neighbour.houses)
        if random.random() < 0.5:
            # Connect house to a battery
            battery = functions.get_random_component(self.neighbour.batteries)
            while battery.capacity < house.capacity and T < 10:
                battery = functions.get_random_component(self.neighbour.batteries)
            self.neighbour.disconnect(house, house.connections[0])
            self.neighbour.connect(house, battery)
            house.state = 1

        else:
            # Connect house to another house
            house2 = functions.get_random_component(self.neighbour.houses)
            if house2 != house: 
                if house.output + house2.output <= house2.connections[0].capacity or T > 10:
                    self.neighbour.disconnect(house, house.connections[0])
                    self.neighbour.connect(house, house2)
    
    def store_solution(self):
        for house in self.neighbour.houses:
            if house.state == 1:
                self.solution.disconnect(house, self.solution[house].connections[0])
                self.solution.connect(house, house.connections[0])
                house.state = 0

    def simulated_annealing(self, max_iter_without_improvement, T0 = 10000, alpha = 0.99):
        self.solution = self.generate_initial_solution()
        self.neighbour = copy.deepcopy(self.solution)
        T = T0
        lowest_cost = 0
        i = 0

        while i < max_iter_without_improvement:
            i += 1
            self.generate_neighbour(T)
            delta = self.neighbour.total_cost - self.solution.total_cost
            if delta < 0 or random.random() < math.exp(-delta / T):
                self.store_solution()
                i = 0
            
            # Temperature cooling
            T = T * alpha 

            if lowest_cost == 0 or self.solution.total_cost < lowest_cost:
                lowest_cost = self.solution.total_cost
                print(lowest_cost)
            #if T < 1e-10:  
                #break

        return self.solution
      