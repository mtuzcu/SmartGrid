# Contains Functions involving random actions
# Mahir Tuzcu - 11070978

import functions
import random as rand
from classes.objects import *

def viability(node1, node2):
    """check if connection node1 to node2 is a viable connection"""
    if node2.connections[2] != None and node1.connections[2] != node2.connections[2]:
       if  node1.capacity + node1.output + node2.connections[2].capacity <= 0:
           return True
       return False
    return True

def improvement(node1, node2):
    """check if connecting node1 to node2 provides a cost improvement"""
    if node1.distance != 0:
        if functions.manhatten_distance(node1, node2) < node1.distance:
            return True
        else:
            return False
    return True

def cross_improvement(node1, node2) -> bool:
    r1 = functions.manhatten_distance(node1, node2.connections[0])
    r2 = functions.manhatten_distance(node2, node1.connections[0])
    if r1 + r2 < node1.distance + node2.distance:
        return True
    return False

def cross_viability(node1, node2):
    output1 = node1.output + node1.capacity
    output2 = node2.output + node2.capacity
    capacity1 = 0
    capacity2 = 0

    if node1.connections[2] != None:
        capacity1 = node1.connections[2].capacity
        capacity1 += - output1 + output2
    if node2.connections[2] != None:
        capacity2 = node2.connections[2].capacity
        capacity2 += - output2 + output1

    if capacity1 <= 0 and capacity2 <= 0:
        return True

def switch_connections(grid, node1, node2):
    """switches node1's and node2's connection points if swap is viable and improves cost"""
    if cross_viability(node1, node2) == True:
        if cross_improvement(node1, node2) == True:
            grid.swap(node1, node2)

def solved(grid):
    """test if current grid is solved and viable"""
    for battery in grid.batteries:
        if battery.capacity > 0:
            return False
    for house in grid.houses:
        if house.connections[2] == None:
            return False
    return True

def check_loop(self, node, node2, stack = None):
    if stack == None:
        stack = [node]
    next_node = node2.connections[0]
    if next_node != None:
        if next_node not in stack:
            stack.append(next_node)
            return self.check_loop(node, next_node, stack)
        else:
            return True
    else:
        return False
    
class shortest_path():
    def __init__(self, grid) -> object:
        
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
                if house.connections[2] == battery:
                    current_battery_network.append(house)
                    house.distance = functions.manhatten_distance(battery, house)
                
            # sort the list containing current battery's network in order from closest
            # house to battery to farthest house. 
            self.battery_networks.append(merge_sort(current_battery_network))

    def optimize_network(self) -> None:
        #for node in self.battery_networks[0]:
            #print(node, node.connections[2], node.state)
        for network in self.battery_networks:
            for i in range(1, len(network)):
                house = network[len(network) - i]
                for another_house in network:
                    if house != another_house and self.check_loop(house, another_house) == False:
                        if functions.manhatten_distance(house, another_house) < functions.manhatten_distance(house, house.connections[0]):
                            self.solution.disconnect(house, house.connections[0])
                            self.solution.connect(house, another_house)      