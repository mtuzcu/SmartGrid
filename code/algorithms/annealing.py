# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.objects import *
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
            battery_queue = copy.copy(batteries)
            battery = functions.get_random_component(battery_queue)
            while battery.capacity + house.output > 0 and len(battery_queue) > 1:  # Ensure battery has enough capacity
                battery_queue.remove(battery)
                battery = functions.get_random_component(battery_queue)
                
            grid.connect(house, battery)
        general.check_solved(grid)
        return grid

    def reset_grid(self, grid):
        for house in grid.houses:
            house.reset()
        for battery in grid.batteries:
            battery.reset()
        grid.total_cost = 0
        return grid

    # Generate neighbor solution
    def generate_neighbour(self, neighbour, T):
        house = functions.get_random_component(neighbour.houses)
        if random.random() < 0.2:
            # Connect house to a battery
            battery_queue = copy.copy(neighbour.batteries)
            battery = functions.get_random_component(battery_queue)
            while len(battery_queue) > 1 and (battery.capacity + house.output + house.capacity < 0 and T < 1):
                battery_queue.remove(battery)
                battery = functions.get_random_component(battery_queue)
            neighbour.disconnect(house, house.connections[0])
            neighbour.connect(house, battery)

        else:
            # Connect house to another house
            house2 = functions.get_random_component(neighbour.houses)
            if house2 != house: 
               # if house2.connections[2] == None or (house2.connections[2].capacity + house.capacity + house.output < 0 or T > 1):
                neighbour.disconnect(house, house.connections[0])
                neighbour.connect(house, house2)
        
    def simulated_annealing(self, max_iter_without_improvement, T0 = 10000, alpha = 0.999):
        current = self.generate_initial_solution(self.grid)
        solution = copy.deepcopy(current)
        neighbour = copy.deepcopy(current)
        T = T0
        lowest_cost = 0
        i = 0

        while i < max_iter_without_improvement:
            i += 1
            self.generate_neighbour(neighbour, T)
            extra = 0
            for house in neighbour.houses:
                if house.connections[2] == None:
                    extra += 10 * house.output
            #general.cleanup(self.neighbour)
            delta = neighbour.total_cost + extra - lowest_cost
            if delta < 0: #or random.random() < math.exp(-delta / T):
                print(neighbour.total_cost)
                self.store_solution(current, neighbour)
  
            # Temperature cooling
            T = T * alpha 
            #print(self.current.total_cost)

            if (lowest_cost == 0 or current.total_cost < lowest_cost): # and general.check_solved(current) == True:
                if lowest_cost == 0:
                    for house in current.houses:
                        if house.connections[2] == None:
                            extra += 10 * house.output
                lowest_cost = current.total_cost + extra
                self.store_solution(solution, current)
                i = 0
                print(lowest_cost)

        print(solution.total_cost)
        #general.shortest_path(self.solution)
        return solution
      
    def run(self, iter, T0 = 10000, alpha = 0.99):
            current = copy.deepcopy(self.grid)
            solution = copy.deepcopy(self.grid)
            lowest_cost = 0
            i = 0
            iter = 100

            while i < iter:
                i += 1
                current = self.reset_grid(current)
                current = self.generate_initial_solution(current)
                if general.check_solved(current) == True:
                    general.shortest_path(current)

                    if lowest_cost == 0 or current.total_cost < lowest_cost:
                        lowest_cost = current.total_cost
                        self.store_solution(solution, current)
                        solution.total_cost = lowest_cost
                        print(lowest_cost * 9)

            return solution
    
    def run2(self):
        current = copy.deepcopy(self.grid)
        mode = 2
        das = 0

        general.get_distances(current)
        for i in range(0, len(current.houses)):
            for battery in current.batteries:
                house = battery.distances[i]
                if battery.capacity + house.output < 0:
                    if house.connections[0] == None:
                        current.connect(house, battery)
                    elif mode == 1:
                        if functions.manhatten_distance(house, battery) < functions.manhatten_distance(house, house.connections[0]):
                            current.disconnect(house, house.connections[0])
                            current.connect(house, battery)

        path = general.shortest_path(current)
        for house in current.houses:
            if house.connections[2] == None and das == 2:
                current.connect(house, functions.get_random_component(current.batteries))
        #path.exhange()

        ad = 1
        if ad == 2:
            hlist = general.longest_connections(current)
            for i in range(0, len(hlist)):
                house1 = hlist[len(hlist) - i - 1]
                for house2 in current.houses:
                    if house1.connections[2] != house2.connections[2] and house1.connections[0] != house1.connections[2]:
                        if functions.manhatten_distance(house1, house2) < house.distance:
                            current.disconnect(house1, house1.connections[0])
                            current.connect(house1, house2)
            general.shortest_path(current)
        
        for house in current.houses:
            if house.connections[0] == None:
                print(house, house.output)
        for battery in current.batteries:
            print(battery.capacity)
                
        return current