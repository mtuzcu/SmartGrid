# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

from classes.grid import *
import functions

class cleanup():

    def __init__(self, grid) -> None:
        
        self.solution = grid
        self.find_networks()
        self.optimize_network()

    def find_networks(self) -> None:

        # generate a list of each batteries' network containing all houses and store 
        # this list inside battery_networks
        self.battery_networks = []
        for battery in self.solution.batteries:
            current_battery_network = [battery]
            for house in self.solution.houses:
                if house.state == 0:
                    if house.connections[2] == battery:
                        current_battery_network.append(house)
                        house.state = functions.euclidean_distance(battery, house)
                
            # sort the list containing current battery's network in order from closest
            # house to battery to farthest house. 
            self.battery_networks.append(merge_sort(current_battery_network))

    def optimize_network(self) -> None:
        for network in self.battery_networks:
            for house in network:
                if house.id == 1:
                    for another_house in network:
                        if house == another_house:
                            break
                        if functions.manhatten_distance(house, another_house) < functions.manhatten_distance(house, house.connections[0]):
                            self.solution.disconnect(house, house.connections[0])
                            self.solution.connect(house, another_house)
            
            for house in network:
                if house.connections[2] == None:
                    print(house)

def merge_sort(list):
    if len(list) > 1:
        mid = len(list) // 2
        left_half = list[:mid]
        right_half = list[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i].state < right_half[j].state:
                list[k] = left_half[i]
                i += 1
            else:
                list[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            list[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            list[k] = right_half[j]
            j += 1
            k += 1

    return list

    






















        
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


    


