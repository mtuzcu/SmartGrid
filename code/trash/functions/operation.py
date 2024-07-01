# Contains Functions involving random actions
# Mahir Tuzcu - 11070978

import functions
import random as rand
import classes

def viability(node1, node2):
    """check if connection node1 to node2 is a viable connection"""
    if node2.connections[2] != None:
        if node1.connections[2] != node2.connections[2]:
            if node1.capacity + node1.output + node2.connections[2].capacity <= 0:
                return 1
            else:
                return 2
        else:
            return 3
    return False

def improvement(node1, node2):
    """check if connecting node1 to node2 provides a cost improvement"""
    if node1 != node2:
        if node1.distance != 0:
            if functions.manhatten_distance(node1, node2) < node1.distance:
                return True
            else:
                return False
        return True
    return False

def cross_improvement(node1, connect1, node2, connect2) -> bool:
    r1 = functions.manhatten_distance(node1, connect1)
    r2 = functions.manhatten_distance(node2, connect2)
    delta = r1 + r2 - (node1.distance + node2.distance)
    return delta

def cross_viability(node1, node2):
    if node1.id == 2 or node2.id == 2:
        return False
    output1 = node1.output + node1.capacity
    output2 = node2.output + node2.capacity
    capacity1 = 1
    capacity2 = 1

    if node1.connections[2] != None:
        capacity1 = node1.connections[2].capacity
        capacity1 += -output1 + output2
    if node2.connections[2] != None:
        capacity2 = node2.connections[2].capacity
        capacity2 += -output2 + output1

    if capacity1 <= 0 and capacity2 <= 0:
        return True
    return False

def swap_connections(grid, node1, node2):
    """switches node1's and node2's connection points if swap is viable and improves cost"""
    if cross_improvement(node1, node2.connections[0], node2, node1.connections[0]) < 0:
        if node1.connections[2] == node2.connections[2]:
            None
        elif cross_viability(node1, node2) == True:
            if cross_improvement(node1, node2.connections[0], node2, node1.connections[0]) < 0:
                grid.swap(node1, node2)
                return True
    return False

def improve_network(grid, node1, node2):
    """switches node1's and node2's connection points if swap is viable and improves cost"""
    if same_network(node1, node2) == True:
            if check_loop(node1, node2) == False:
                if improvement(node1, node2) == True:
                    grid.disconnect(node1)
                    grid.connect(node1, node2)
            else:
                if cross_improvement(node1, node2, node2, node1.connections[0]) < 0:
                    anchor = node1.connections[0]
                    grid.disconnect(node1)
                    grid.disconnect(node2)
                    grid.connect(node1, node2)
                    grid.connect(node2, anchor)

def new_connection(grid, node1, node2):
    if improvement(node1, node2) == True:
        case = viability(node1, node2)
        if case == 1:
            grid.disconnect(node1, node1.connections[0])
            grid.connect(node1, node2)   
        if case == 2:
            options = None
            battery1 = node1.connections[2]
            battery2 = node2.connections[2]
            if battery1 != None and battery2 != None:
                if battery1 != battery2:
                    for house2 in battery2.connections[3]:
                        if house2 != node2 and house2.id != 2:
                            if cross_viability(node1, house2) == True:
                                for house1 in battery1.connections[3]:
                                    if house1 != node1 and house1 != house2:
                                        if check_loop(node1, house1) == False and check_loop(house2, node2) == False:
                                            delta = cross_improvement(node1, node2, house2, house1)
                                            if delta <= 0:
                                                options = functions.dynamic_list((house2, house1), delta, options)

            if options != None and len(options[0]) > 0:
                options = options[0]
                grid.disconnect(node1)
                grid.connect(node1, node2)
                grid.disconnect(options[0][0], options[0][0].connections[0])
                grid.connect(options[0][0], options[0][1])

        if case == 3:
            if swap_connections(grid, node1, node2) == True:
                print('yauw')
    return False

def solved(grid):
    """test if current grid is solved and viable"""
    for battery in grid.batteries:
        if battery.capacity > 0:
            return False
    for house in grid.houses:
        if house.connections[2] == None:
            return False
    return True

def same_network(node1, node2):
    if node1.connections[2] == node2.connections[2]:
        return True
    return False

def check_loop(node, node2, stack = None):
    if stack == None:
        stack = [node]
    next_node = node2.connections[0]
    if next_node != None:
        if next_node not in stack:
            stack.append(next_node)
            return check_loop(node, next_node, stack)
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
            self.battery_networks.append(current_battery_network)

    def optimize_network(self) -> None:
        #for node in self.battery_networks[0]:
            #print(node, node.connections[2], node.state)
        for network in self.battery_networks:
            for i in range(1, len(network)):
                house = network[len(network) - i]
                for another_house in network:
                    if house != another_house and check_loop(house, another_house) == False:
                        if functions.manhatten_distance(house, another_house) < functions.manhatten_distance(house, house.connections[0]):
                            self.solution.disconnect(house, house.connections[0])
                            self.solution.connect(house, another_house)      


def optimize_network(grid, network) -> None:
        #for node in self.battery_networks[0]:
            #print(node, node.connections[2], node.state)
        for i in range(1, len(network)):
            house = network[len(network) - i]
            for another_house in network:
                if house != another_house and check_loop(house, another_house) == False:
                    if functions.manhatten_distance(house, another_house) < functions.manhatten_distance(house, house.connections[0]):
                        grid.disconnect(house, house.connections[0])
                        grid.connect(house, another_house) 



def next_point(a, b):
    if a < b:
        return a + 1
    return a - 1
