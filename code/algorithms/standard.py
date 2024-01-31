# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
from functions.distance import *
from functions.Random import *

def random_algorithm(Grid: object, component: object):
    """random algorithm"""

    # select random component to connect to
    random_component = get_random_component(component)
    
    # connect component with the new random_component
    Grid.connect_components(random_component, component)

def astar(grid: Grid, start: Node, end: Node):
    """astar aglorithm"""
    open_set = []
    heapq.heappush(open_set, start)
    cost = 0
    h = manhatten_distance(start, end)

    while open_set:
        current = heapq.heappop(open_set)
        if current.x == goal.x and current.y == goal.y:
            return reconstruct_path(current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_x, next_y = current.x_coordinate + dx, current.y_coordinate + dy

            if 0 <= next_x < grid.size and 0 <= next_y < grid.size:
                next_node = grid[next_x][next_y]
                tentative_cost = current_cost + 1
                if tentative_g < next_node.g:
                    next_node.g = tentative_g
                    next_node.h = manhattan_distance(next_node, goal)
                    next_node.parent = current
                    heapq.heappush(open_set, next_node)


    


