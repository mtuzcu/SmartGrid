# contains functions to determine distances
# Mahir Tuzcu - 11070978

import functions
import random as rand
import classes

def manhatten_distance(node1, node2) -> int:
    """returns manhatten distance between node1 and node2. Input can either be an object or
    the (x, y) coordinates in tuple format of the object"""
    if node1 == None or node2 == None:
        return float('inf')
    cords1 = node1.cords
    cords2 = node2.cords
    distance = (abs(cords1[0] - cords2[0]) + abs(cords1[1] - cords2[1]))
    return distance

def get_neighbours(cords, size):
    """returns list of neighbouring (x, y) coordinate in tuple form if they are within bounds"""
    neighbours = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_x, next_y = cords[0] + dx, cords[1] + dy
        if 0 <= next_x < size and 0 <= next_y < size:
            neighbours.append((next_x, next_y))
    return neighbours

def get_closet_node(node1, battery):
    """get closest node in battery network to input house0"""
    closest_node = battery 
    closest_distance = manhatten_distance(node1, battery)
    for node2 in battery.houses:
        if manhatten_distance(node1, node2) < closest_distance:
            closest_node = node2
    return closest_node

def unique_nodes(grid):
    """gets 2 random and unique house nodes from grid"""
    if isinstance(grid, list):
        list1 = grid
    else:
        list1 = grid.houses
    house1 = functions.get_random_component(list1)
    house2 = functions.get_random_component(list1)
    while house1 == house2:
        house2 = functions.get_random_component(list1)
    return house1, house2

def random(start = 0, end = 1) -> float:
    """returns a random float between[start, end]"""
    random_float = rand.randint(start, end)
    return random_float

def select_random_index(N_candidates: int) -> int:
    """takes a number of candidates to randomly choose between and returns an index i"""    
    random_int = rand.randrange(0, N_candidates)
    return random_int

def get_random_component(candidates_list: list) -> object:
    """returns a randomly chosen component from list of eligible components"""
    index = select_random_index(len(candidates_list))
    return candidates_list[index]

def get_viable_batteries(grid, house) -> list:
    """returns a list of all battery nodes that can accomodate house"""
    viable_batteries = []
    for battery in grid.batteries:
        if battery.viability(house) == True:
            viable_batteries.append(battery)
    return viable_batteries

def find_cable(node1, node2):
    """Returns the cable connecting node1 and node2. Returns false if it 
    does not exist"""
    if check_nodes(node1, node2) == True:
        if node1 != node2:
            temp_cable = classes.Cable(node1, node2)
            if temp_cable in node1.cables:
                for cable in node1.cables:
                    if cable == temp_cable:
                        return cable
    return None

def get_random_cables(grid):
    cable_list = list(grid.cables)
    cable1, cable2 = rand.sample(cable_list, 2)
    return cable1, cable2

def scan_network(node, data = False):
    if data == False:
        # data contains the following: [capacity, cost, cables, houses, battery]
        data = [0, 0, set(), set(), None]
    if len(node.cables) == 0:
        return False
    for cable in node.cables:
        if data != False:
            if node not in data[3]:
                if isinstance(node, classes.Battery):
                    if data[4] == None or data[4] == node:
                        data[4] = node
                    else: 
                        return False
                else:
                    data[0] += node.output
                data[3].add(node)
                
            if cable not in data[2]:
                data[2].add(cable) 
                data[1] += cable.cost
                next_node = cable.other(node)
                data = scan_network(next_node, data) 
    return data

def analyse_network(node):
    data = scan_network(node)
    if data != False:
        if data[4] != None:
            if data[4] in data[3]:
                data[3].remove(data[4])
            
            # check capacity of battery
            if data[4].max_capacity + data[0] <= 0:
                return data
    return False

def check_nodes(component1, component2):
    """returns True if both component1 and component2 are either a Battery or House object. 
    Otherwise returns False"""
    if isinstance(component1, (classes.House, classes.Battery)) and isinstance(component2, (classes.House, classes.Battery)):
        return True
    return False

def legal_connection(node1, node2):
    if isinstance(node1, classes.Battery) and isinstance(node2, classes.Battery):
        return False
    if node1 == node2:
        return False
    if isinstance(find_cable(node1, node2), classes.Cable):
        return False
    return True

def next_point(a, b):
    if a < b:
        return a + 1
    return a - 1


