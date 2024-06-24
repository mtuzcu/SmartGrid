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

        while i < iter:
            i += 1
            h1, h2 = functions.unique_nodes(current)
            functions.switch_connections(current, h1, h2)
            print(current.total_cost)

        return current

            
            







        # while running:
        # closest connection
        # check swap
