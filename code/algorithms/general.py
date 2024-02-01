# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
from functions.distance import *
from functions.Random import *

def random_algorithm(Grid: object, component: object):
    """random algorithm"""

    # select random component to connect to
    random_component = get_inverse_component(Grid, component)
    # connect component with the new random_component
    Grid.connect_end_components(random_component, component)

    return random_component

def astar(grid: Grid, start: Node, end: Node):
    """astar aglorithm"""
    open_set = []
    heapq.heappush(open_set, start)

    while open_set:
        current = heapq.heappop(open_set)
        if current.x_coordinate == end.x_coordinate and current.y_coordinate == end.y_coordinate:
            print("cable set")
        
        for next_x, next_y in get_neighbours(current.x_coordinate, current.y_coordinate, grid.size):
            next_node = grid[next_x][next_y]
            g_value = calc_g(start, next_node)
            print(g_value, next_node.g)
            if g_value > next_node.g:
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


    


