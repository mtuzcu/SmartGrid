# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import numpy as np
import functions

cable_cost = 9

class Edge:
        """cable object containing data for instanced cable. Multiple cables per node possible"""
        def __init__(self, node_1, node_2, cost = 1):
            self.node1 = node_1
            self.node2 = node_2
            self.cost = cost * cable_cost * functions.manhatten_distance(self.node1.cords, self.node2.cords)
            self.capacity = min(self.node1.capacity, self.node2.capacity)
            self.flow = 0
        
        def other_node(self, current_node):
            return self.node2 if current_node == self.node1 else self.node1
    
class Node:
    def __init__(self, grid, cords: tuple):
        """Node on grid containing node data"""
        self.grid = grid
        self.cords = cords
        self.edges: list = []
        self.cables: list = []
        self.capacity = 0
        self.id = 0

        # algorithm attributes
        self.h = 0
        self.g = 0
        self.distance = float('inf')
        self.parent: Node = None
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def add_object(self, object_id, capacity = 0):
        """Adds a component to the Node. Adds  house if object_id = 1, battery 
        if object_id = 2 or a cable if object_id = Cable object."""
        if isinstance(object_id, Edge):
            self.edges.append(object_id)
        else:
            self.id = object_id
            self.capacity = capacity
        if object_id == 1:
            self.grid.houses.append(self)
        if object_id == 2:
            self.grid.batteries.append(self)
       
    
    def remove_object(self, object_id):
        """removes a cable from the node. If object_id = cable object, removes
        that specific cable. Otherwise removes all cables from node."""
        if isinstance(object_id, Edge):
            self.edges.remove(object_id)
        else:
            self.edges = []  

    def __hash__(self):
        return hash(self.cords)

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.cords) == (other.cords)
        return False

    def __repr__(self):
        type_list = ['House', 'Battery', 'Super Node']
        return f"{type_list[self.id - 1]}{self.cords},{self.distance}"

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []
        self.edges: list = []
        self.cables: list = []
        self.nodes: list = []
        self.unconnected_houses: list = []

        # attributes
        self.size = 0
        self.N_houses: int
        self.N_batteries: int
        self.N_connected_houses: int = 0
        self.N_connected_batteries: int = 0

        # stats
        self.total_cost_cables = 0
    
    def connect(self, node1: object, node2: object, type = 0, cost = 1):
        """Creates a cable object and connects it to Node1 and Node2"""
        new_edge = Edge(node1, node2, cost)
        if type == 0:
            node1.add_object(new_edge)
            node2.add_object(new_edge)
            self.edges.append(new_edge)
        else:
            self.cables.append(new_edge)
        #self.update_stats(new_edge, 0)
    
    def disconnect(self, edge):
        """removes an edge"""
        #self.update_stats(edge, 1)
        edge.node1.remove_object(edge)
        edge.node2.remove_object(edge)
        self.edges.remove(edge)
        del edge

    def update_stats(self, cable, sign):
        """update costs and capacity of house and battery. If sign = 0,
        adds the stats, if signs = 1, removes the stats"""
        sign = (-1)**sign
        self.total_cable_cost += sign * cable.cost

        if cable.node1.id == 1 and cable.node2.id == 2:
            cable.node2.capacity += sign * cable.node1.capacity
            self.update_houses(cable.node1, sign)
        if cable.node1.id == 2 and cable.node2.id == 1:
            cable.node1.capacity += sign * cable.node2.capacity
            self.update_houses(cable.node2, sign)

    def update_houses(self, node, sign):
        if sign == 1 and node in self.unconnected_houses: 
            self.unconnected_houses.remove(node) 
        elif node not in self.unconnected_houses: 
            self.unconnected_houses.append(node)

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
        self.nodes = [[Node(self, (x, y)) for y in range(size_y)] for x in range(size_x)]
    
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
                        if sign == 0:
                            x = int(row[0])
                            y = int(row[1])
                            capacity = float(row[2])

                            # set node at (x, y) as house
                            self.nodes[x][y].add_object(1, capacity)
                            self.unconnected_houses.append(self.nodes[x][y])
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])

                            # set node at (x, y) as battery
                            self.nodes[x][y].add_object(2, capacity)
            

            self.N_houses = len(self.houses)
            self.N_batteries = len(self.batteries)
            
            # if data input successful 
            if nodes == self.N_houses + self.N_batteries:
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
                
                
                    
      
        
        