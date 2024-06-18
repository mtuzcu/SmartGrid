# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import numpy as np
import functions

cable_cost = 9

class Cable:
        """cable object containing data for instanced cable. Multiple cables per node possible"""
        def __init__(self):
            self.connection1: Node
            self.connection2: Node
            self.cost = 0 
            self.charge = 0

        def modify_connection(self, node1, node2):
            """Changes which battery the cable is connected to"""
            self.connection1 = node1
            self.connection2 = node2
            self.update()

        def update(self):
            """calculates the cost of the cable and the electric current going through it.
            If charge equals 0, it means the cable is able to transfer all capacity from connected
            houses to a connected battery"""
            self.cost = cable_cost * functions.manhatten_distance(self.connection1.cords, self.connection2.cords)

    
class Node:
    def __init__(self, grid, cords: tuple):
        """Node on grid containing node data"""
        self.grid = grid
        self.cords = cords
        self.cables: list = []
        self.property = None
        self.network = 0
        self.id = 0

        # astar attributes
        self.h = 0
        self.g = 0
        self.parent: Node = None
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def add_object(self, object_id, property = 0):
        """Adds a component to the Node. Adds  house if object_id = 1, battery 
        if object_id = 2 or a cable if object_id = Cable object."""
        if object_id == 1:
            self.id = 1
            self.property = property
            self.grid.houses.append(self)
        if object_id == 2:
            self.id = 2
            self.property = -property
            self.grid.batteries.append(self)
        if isinstance(object_id, Cable):
            self.cables.append(object_id)
    
    def remove_object(self, object_id):
        """removes a cable from the node. If object_id = cable object, removes
        that specific cable. Otherwise removes all cables from node."""
        if isinstance(object_id, Cable):
            self.cables.remove(object_id)
        else:
            self.cables = []  

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []
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
        self.total_cable_cost = 0
    
    def connect(self, node1: object, node2: object):
        """Creates a cable object and connects it to Node1 and Node2"""
        new_cable = Cable()
        new_cable.modify_connection(node1, node2)
        node1.add_object(new_cable)
        node2.add_object(new_cable)
        self.cables.append(new_cable)
        self.update_stats(new_cable, 0)
    
    def disconnect(self, cable):
        """removes a cable"""
        self.update_stats(cable, 1)
        cable.connection1.remove_object(cable)
        cable.connection2.remove_object(cable)
        self.cables.remove(cable)
        del cable

    def update_stats(self, cable, sign):
        """update costs and capacity of house and battery. If sign = 0,
        adds the stats, if signs = 1, removes the stats"""
        sign = (-1)**sign
        self.total_cable_cost += sign * cable.cost

        if cable.connection1.id == 1 and cable.connection2.id == 2:
            cable.connection2.property += sign * cable.connection1.property
            self.update_houses(cable.connection1, sign)
        if cable.connection1.id == 2 and cable.connection2.id == 1:
            cable.connection1.property += sign * cable.connection2.property
            self.update_houses(cable.connection2, sign)

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
                
                
                    
      
        
        