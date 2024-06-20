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
        self.cords = cords
        self.connections = [[],[]]
        self.cost = 0
        self.state = 0

    def modify(self, id, output, capacity):
        self.id = id
        self.output = output
        self.capacity = capacity

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
        node1.connections[0].append(node2)
        node2.connections[1].append(node1)

    def disconnect(self, node1: object, node2: object):
        """Removes a connection between node1 (house) and node2 (house or battery)"""
        node1 = functions.get_node(self, node1)
        node2 = functions.get_node(self, node2)
        node1.connections[0].remove(node2)
        node2.connections[1].remove(node1)

    def update_stats(self, node1, node2, sign):
        """update costs and capacity of house and battery. If sign = 0,
        adds the stats, if signs = 1, removes the stats"""
        sign = (-1)**sign
        node1.cost = 9 * functions.manhatten_distance(node1, node2)
        self.total_cost += sign * node1.cost

        if edge.node1.id == 1 and edge.node2.id == 2:
            edge.node2.capacity += sign * edge.node1.capacity
        if edge.node1.id == 2 and edge.node2.id == 1:
            edge.node1.capacity += sign * edge.node2.capacity

    # MAGIC METHODS
    def __getitem__(self, coordinates):
        """allows the use of grid[x, y] to return the node at (x, y)"""
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
                
                
                    
      
        
        