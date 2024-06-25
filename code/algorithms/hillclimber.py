import heapq
from classes.objects import *
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
        iter = 100000
        i = 0
        lowest_cost = 0

        while i < iter:
            i += 1
            h1, h2 = functions.unique_nodes(current)
            functions.new_connection(current, h1, h2)
            #functions.shortest_path(current)

            if lowest_cost == 0 or current.total_cost < lowest_cost:
                lowest_cost = current.total_cost
                print(lowest_cost)

        return current

            
            







        # while running:
        # closest connection
        # check swap
