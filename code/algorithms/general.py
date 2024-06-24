# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

from classes.objects import *
import functions


# Generate initial solution
def innitial(grid):
    houses = grid.houses
    for house in houses:
        battery = functions.get_viable_batteries(house)[0]
        grid.connect(house, battery)
    return grid

def proxy_solution(grid):
      for battery in grid.batteries:
          battery.distances = functions.get_distances(battery, 1)
      for i in range(1, len(grid.houses)):
            for battery in grid.batteries:
                house = battery.distances[i]
                if functions.viability(house, battery):
                    if house.connections[0] == None:
                        grid.connect(house, battery)
                    elif functions.improvement(house, battery):
                        grid.disconnect(house, house.connections[0])
                        grid.connect(house, battery)

def untangle(grid):
    hlist = functions.longest_connections(grid)
    for i in range(0, len(hlist)):
        house1 = hlist[len(hlist) - i - 1]
        for house2 in grid.houses:
            if house1.connections[2] != house2.connections[2] and house1.connections[0] != house1.connections[2]:
                if functions.improvement(house1, house2):
                    grid.disconnect(house1, house1.connections[0])
                    grid.connect(house1, house2)


    

    










def testo(district):
    h = district.houses[0]
    h2 = district.houses[1]
    h3 = district.houses[2]
    h4 = district.houses[3]
    h5 = district.houses[4]
    b = district.batteries[0]
  
    district.connect(h, b)
    district.connect(h2, h)
    district.connect(h3, h2)
    district.disconnect(h, b)
    district.connect(h2,b)
    print('-----')

    print(h, h.capacity, h.output, h.connections)
    print(h2, h2.capacity, h2.output, h2.connections)
    print(h3, h3.capacity, h3.output, h3.connections)
    print(b, b.capacity, b.output, b.connections)

















        
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


    


