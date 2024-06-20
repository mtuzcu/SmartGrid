# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import heapq
from classes.grid import *
import functions

def random_algorithm(grid):
    """random algorithm"""

    # select random component to connect to
    houses = grid.houses
    if len(grid.unconnected_houses) > 0:
        houses = grid.unconnected_houses

    house = functions.get_random_component(houses)
    battery = functions.get_random_component(grid.batteries)
    
    if len(grid.unconnected_houses) > 0:
        i = 0
        while battery.property + house.property > 0 and i < len(grid.batteries):
            battery = functions.get_random_component(grid.batteries)
            i += 1
        
    grid.connect(house, battery)

    if len(house.cables) > 1:
        grid.disconnect(functions.get_random_component(house.cables))
    if battery.property > 0:
        grid.disconnect(functions.get_random_component(battery.cables))

# shortest path
def shortest_path(grid, source, sink):
    dist = {node: float('inf') for row in grid.nodes for node in row}
    parent = {node: None for row in grid.nodes for node in row}
    in_queue = {node: False for row in grid.nodes for node in row}
       
    dist[source] = 0
    queue = [(0, source)]
    
    while queue:
        distance, u = heapq.heappop(queue)
        if in_queue[u]:
            continue
        in_queue[u] = True
        
        for cable in u.cables:
            if cable.node1 == u:
                v = cable.node2
            else:
                v = cable.node1
            
            if cable.capacity > cable.flow and dist[v] > dist[u] + cable.cost:
                dist[v] = dist[u] + cable.cost
                parent[v] = u
                heapq.heappush(queue, (dist[v], v))
    
    return dist, parent

def set_edges(grid):
    for house in grid.houses:
        for battery in grid.batteries:
            grid.connect(house, battery)
            












        
# Astar
def astar(grid: Grid, start: Node, end: Node):
    """astar aglorithm"""
    open_set = []
    heapq.heappush(open_set, start)

    while open_set:
        current = heapq.heappop(open_set)
        if current.cords == end.cords:
            print("cable set")
        
        for (x1, y1) in get_neighbours(current.cords, grid.size):
            next_node = grid[x1][y1]
            g_value = calc_g(start, next_node)
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


    


