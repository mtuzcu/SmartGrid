# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import numpy as np
import functions

cable_cost = 9

class Node:
    def __init__(self, cords):
        """Node on grid containing node data"""
        self.id = 0
        self.cords = cords
        self.connections = [None, [], None]
        self.cost = 0
        self.distance = 0

    def modify(self, id, output, capacity):
        self.id = id
        self.output = output
        self.capacity = capacity
        if id == 2:
            self.connections[2] = self
        self.base = [self.output, self.capacity, self.connections[2]]
    
    def reset(self):
        self.output = self.base[0]
        self.capacity = self.base[1]
        self.connections = [None, [], self.base[2]]

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.cords) == (other.cords)
        return False

    def __repr__(self):
        type_list = ['node', 'House', 'Battery']
        return f"{type_list[self.id]}{self.cords}"

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []
        self.nodes: list = []

        # stats
        self.total_cost = 0
    
    def connect(self, node1: Node, node2: Node):
        """Creates a connection between node1 (house) and node2 (house or battery)"""
        node1 = functions.get_node(self, node1)
        node2 = functions.get_node(self, node2)
        node1.connections[0] = node2
        node2.connections[1].append(node1)
        node1.connections[2] = node2.connections[2]
        self.update_stats(node1, node2, 0)
        self.update_network(node1)

    def disconnect(self, node1: object, node2: object):
        """Removes a connection between node1 (house) and node2 (house or battery)"""
        node1 = functions.get_node(self, node1)
        node2 = functions.get_node(self, node2)
        node1.connections[0] = None
        node2.connections[1].remove(node1)
        node1.connections[2] = None
        self.update_stats(node1, node2, 1)
        self.update_chain(node1, node1)

    def update_stats(self, node1, node2, sign):
        """update costs and capacity of house and battery. If sign = 0,
        adds the stats, if signs = 1, removes the stats"""
        if sign == 0:
            node1.cost = 9 * functions.manhatten_distance(node1, node2)
            node2.capacity += node1.output
            self.total_cost += node1.cost
        if sign == 1:
            self.total_cost += -node1.cost
            node1.cost = 0
            node2.capacity += -node1.output

    def update_network(self, node):
        last_node = self.last_node(node)
        self.update_chain(node, last_node)

    def update_chain(self, node, last_node, stack = []):
        stack.append(node)
        if len(node.connections[1]) > 0:
            for connected_node in node.connections[1]:
                if connected_node not in stack:
                    connected_node.connections[2] = last_node
                    stack.append(connected_node)
                    self.update_chain(connected_node, last_node, stack)

    def last_node(self, node, stack = []):
        stack.append(node)
        node = node.connections[0]
        if node == None:
            return None
        if node.id == 1:
            if node not in stack:
                node = self.last_node(node, stack)
            else:
                return None
        return node

    # MAGIC METHODS
    def __getitem__(self, coordinates):
        """allows the use of grid[x, y] to return the node at (x, y)"""
        if coordinates == None:
            return None
        if isinstance(coordinates, Node):
            x, y = coordinates.cords
        else:
            x, y = coordinates
        return self.nodes[x][y]

    def __setitem__(self, coordinates, node):
        """stores a node in nested list nodes at coordinate (x, y)"""
        x, y = coordinates
        self.nodes[x][y] = node

    # ==================================================================
    # Functions below are used to generate the grid. 
    # This is only used once at the start 
    # ==================================================================
    
    def create_grid(self, size_x, size_y):
        """Creates a size_x by size_y grid of nodes"""
        self.houses.clear()
        self.batteries.clear()
        self.nodes.clear()
        self.size = size_x
        self.nodes = [[Node((x, y)) for y in range(size_y)] for x in range(size_x)]
    
    def fill_grid(self, district_file_path):
        """generates a grid of nodes filed with houses and batteries according
        to the data given in csv_file."""

        # Get a list of all files in the directory
        file_list = os.listdir(district_file_path)  

        # Filter the list to include only CSV files
        self.csv_files = [file for file in file_list if file.endswith('.csv')]  

        if self.csv_files:
            nodes = 0
            # Iterate through each CSV file
            for csv_file in self.csv_files:
                # Construct the full path to the CSV file
                csv_file_path = os.path.join(district_file_path, csv_file)

                # open csv file
                with open(csv_file_path, 'r') as file:
                    csv_reader = csv.reader(file)

                    # Skip the header row
                    header = next(csv_reader)
                    
                    # change sign based on if current csv file contains house or battery data
                    # 0 for a house and 1 for a battery
                    sign = 0 if len(header) > 2 else 1
                    
                    # itterate through rows of csv file 
                    for row in csv_reader:
                        nodes += 1

                        # set node at (x, y) as house
                        if sign == 0:
                            x = int(row[0])
                            y = int(row[1])
                            output = float(row[2])
                            self.nodes[x][y].modify(1, output, 0)
                            self.houses.append(self.nodes[x][y])

                        # set node at (x, y) as battery
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])
                            self.nodes[x][y].modify(2, 0, capacity)
                            self.batteries.append(self.nodes[x][y])
            
            # if data input successful 
            if nodes == len(self.houses) + len(self.batteries):
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
                
                
                    
      
        
        