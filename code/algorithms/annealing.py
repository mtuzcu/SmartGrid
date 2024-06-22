# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
import functions
import copy
import math
import random
from algorithms import general
import functions.simulation

class annealing():

    def __init__(self, grid) -> None:
        self.grid = grid

    # Generate initial solution
    def generate_initial_solution(self, grid, type = 0):
        houses = grid.houses
        batteries = grid.batteries
        for house in houses:
            battery = functions.get_random_component(batteries)
            while battery.capacity < house.capacity:  # Ensure battery has enough capacity
                battery = functions.get_random_component(batteries)
            grid.connect(house, battery)
        return grid

    def reset_grid(self, grid):
        for house in grid.houses:
            house.reset()
        for battery in grid.batteries:
            battery.reset()
        grid.total_cost = 0
        return grid

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

        else:
            # Connect house to another house
            house2 = functions.get_random_component(self.neighbour.houses)
            if house2 != house: 
                if house.output + house2.output <= house2.connections[0].capacity or T > 10:
                    self.neighbour.disconnect(house, house.connections[0])
                    self.neighbour.connect(house, house2)
    
    def store_solution(self, grid1, grid2):
        for row in grid2.nodes:
            for node in row:
                if node.id != 0:
                    node1 = grid1[node]
                    node1.connections[0] = grid1[node.connections[0]]
                    node1.connections[2] = grid1[node.connections[2]]
                    node1.connections[1] = []
                    for item in node.connections[1]:
                        node1.connections[1].append(grid1[item])
                    node1.capacity = node.capacity
                    node1.output = node.output

    def simulated_annealing(self, max_iter_without_improvement, T0 = 10000, alpha = 0.99):
        self.current = self.generate_initial_solution()
        self.solution = copy.deepcopy(self.current)
        self.neighbour = copy.deepcopy(self.current)
        T = T0
        lowest_cost = 0
        i = 0

        while i < max_iter_without_improvement:
            i += 1
            self.generate_neighbour(T)
            #general.cleanup(self.neighbour)
            delta = self.neighbour.total_cost - self.current.total_cost
            if delta < 0 or random.random() < math.exp(-delta / T):
                self.store_solution(self.current, self.neighbour)
  
            # Temperature cooling
            T = T * alpha 

            if lowest_cost == 0 or self.current.total_cost < lowest_cost:
                lowest_cost = self.current.total_cost
                self.store_solution(self.solution, self.current)
                i = 0
                print(lowest_cost)

        print(self.solution.total_cost)
        general.cleanup(self.solution)
        return self.solution
      
    def run(self, max_iter_without_improvement, T0 = 10000, alpha = 0.99):
            current = copy.deepcopy(self.grid)
            solution = copy.deepcopy(self.grid)
            lowest_cost = 0
            i = 0

            while i < max_iter_without_improvement:
                print(i)
                i += 1
                current = self.reset_grid(current)
                current = self.generate_initial_solution(current)
                general.cleanup(current)

                if lowest_cost == 0 or current.total_cost < lowest_cost:
                    lowest_cost = current.total_cost
                    self.store_solution(solution, current)
                    solution.total_cost = lowest_cost
                    print(lowest_cost)

            return solution