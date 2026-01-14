import heapq
import functions
import copy
import math
import random
import algorithms

class hclimber:
    def __init__(self, grid) -> None:
        self.grid = grid
    
    def run(self):
        current = copy.deepcopy(self.grid)
        neighbour = copy.deepcopy(self.grid)
        algorithms.innitial(current)
        N_houses = len(current.houses)

        iter = 100
        i = 0
        lowest_cost = 0

        while i < iter:
            i += 1
            #print(i)
            functions.get_cable_distances(current)
            for i in range(0, N_houses - 1):
                h1 = current.houses[i]
                for h2 in current.houses:
                    if h1 != h2:
                        functions.improve_network(current, h1, h2)
            functions.get_cable_distances(current)

            #h1, h2 = functions.unique_nodes(current)
            #functions.new_connection(current, h1, h2)
            #functions.shortest_path(current)
            #functions.swap_within_network(current, h1, h2)
            #functions.solved(current)


            if lowest_cost == 0 or current.total_cost < lowest_cost:
                lowest_cost = current.total_cost
                print(lowest_cost)

        return current

            
            







        # while running:
        # closest connection
        # check swap
