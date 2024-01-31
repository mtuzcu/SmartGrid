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
    Grid.connect_end_components(random_component, component)

    return random_component

def astar(grid: Grid, start: Node, end: Node):
    """astar aglorithm"""
    open_set = []
    heapq.heappush(open_set, start)
    cost = 0
    h = manhatten_distance(start, end)

    while open_set:
        current = heapq.heappop(open_set)
        if current.x == end.x and current.y == end.y:
            print("cable set")
        
        for next_x, next_y in get_neighbours(current.x, current.y, grid.size):
            next_node = grid[next_x][next_y]
            g_value = calc_g(start, next_node)
            if g_value < next_node.g:
                next_node.g = g_value
                next_node.h = calc_h(next_node, end)
                next_node.parent = current
                heapq.heappush(open_set, next_node)

def calc_g(node_start, node_current):
    return manhatten_distance(node_start, node_current) * 9

def calc_h(node_current, node_end):
    return euclidean_distance(node_current, node_end)

def calc_f(g, h):
    return g + h


    


