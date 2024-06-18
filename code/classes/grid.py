# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import numpy as np
import functions

cable_cost = 9

class Standard_Object:
        def __init__(self, cords, node, max_property = 0):
            """Template for a standard grid object. Property depends on the object
            for houses and batteries it means remaining output/capacity. For cables it
            means 1 if cable is charged and 0 if not."""
            self.cords = cords
            self.node = node
            self.property = 0
            self.max_property = max_property
            self.end_connections: list = []
            self.connected_neighbours: list = []
        
        def move_location(self, new_cords):
            """Moves the object to the new x, y coordinate"""
            self.cords = new_cords
        
        def modify_end_connection(self, operation, connected_object):
            """Adds or removes connected_objects to list of objects this object is end_connected to.
            use operation = 0 to add and 1 to remove the connected_object.
            end_connected means the connected battery or house at the end of a cable connection."""
            if connected_object not in self.end_connections and operation == 0:
                self.end_connections.append(connected_object)
            if connected_object in self.end_connections and operation == 1:
                self.end_connections.pop(connected_object)
        
        def modify_property(self, new_property): 
            """Changes the property for the object. For houses and batteries this means 
            remaining output/capacity. For cables it means 1 for charged and 0 for unused"""
            if self.max_property - new_property >= 0:
                self.property = new_property
                return 0
            else:
                return 1
            
        def is_end_connected(self):
            """returns 1 if object has an end connection. Otherwise returns 0"""
            if len(self.end_connections) == 0:
                return 0
            return 1
        
        def modify_connected_neighbours(self, operation, connected_neighbour):
            """Adds or removes connected_neighbour to list of objects this object is connected to.
            use operation = 0 to add and 1 to remove the connected_neighbour."""
            if connected_neighbour not in self.connected_neighbours and operation == 0:
                self.end_connections.append(connected_neighbour)
            if connected_neighbour in self.connected_neighbours and operation == 1:
                self.end_connections.pop(connected_neighbour)
        
        def __hash__(self):
            # Assuming 'value' is immutable (e.g., an integer)
            return hash(self.cords)

class House(Standard_Object):
        """House objet containing data for instanced house. Only 1 house per node"""
     
class Battery(Standard_Object):
        """Battery object containing data for instanced battery. Only 1 battery per node"""

class Cable:
        """cable object containing data for instanced cable. Multiple cables per node possible"""
        def __init__(self, cords):
            self.cords = cords
            self.endpoint_cords: tuple
            self.connected_house: House
            self.connected_battery: Battery
            self.cost = 0 

        def modify_connection(self, Battery):
            """Changes which battery the cable is connected to"""
            self.connected_battery = Battery
            self.endpoint_cords = Battery.cords
            self.get_cost()

        def get_cost(self):
            """calculates the cost of the battery"""
            self.cost = cable_cost * functions.euclidean_distance(self.cords, self.endpoint_cords)
    
class Node:
    def __init__(self, grid, cords: tuple):
        """Node on grid containing node data"""
        self.grid = grid
        self.cords = cords
        self.battery: object = None
        self.house: object = None
        self.cables: list = []

        # astar attributes
        self.h = 0
        self.g = 0
        self.parent: Node = None
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def add_object(self, object_id, max_property = 0):
        """Adds a house or battery object if node not already occupied by said object
        object_id is 1 for a house and 2 for a battery and 3 for a cable dictionairy.
        If object_id refers to an already instanced object, that object will be added."""
        if (object_id == 1 or isinstance(object_id, House)) and not self.house:
            if isinstance(object_id, House):
                self.house = object_id
            else:
                self.house = House(self.cords, self, max_property)
        if (object_id == 2 or isinstance(object_id, Battery)) and not self.battery:
            if isinstance(object_id, Battery):
                self.battery = object_id
            else:
                self.battery = Battery(self.cords, self, max_property)
        if (object_id == 3 or isinstance(object_id, Cable)):
            if isinstance(object_id, Cable):
                self.cables.append(object_id)
            else:
                object_id = Cable(self.cords)
                self.cables.append(object_id)
            self.grid.cables.append(object_id)
            return object_id
    
    def remove_object(self, object_id):
        """removes a house or battery object if node not already occupied by said object
        object_id is 0 to remove all objects, 1 for a house, 2 for a battery, 3 for a cable.
        if a cable object reference is used for object_id, that specific cable will be 
        removed."""
        if isinstance(object_id, Cable):
            self.grid.total_cable_cost += -object_id.cost
            self.cables.remove(object_id)
            self.grid.cables.remove(object_id)
        else:
            if object_id in (0, 1):
                self.house = None
            if object_id in (0, 2):
                self.battery = None
            if object_id in (0, 3):
                self.cables = None

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []
        self.cables: list = []
        self.nodes: list = []

        # attributes
        self.size = 0
        self.N_houses: int
        self.N_batteries: int
        self.N_connected_houses: int = 0
        self.N_connected_batteries: int = 0

        # stats
        self.total_cable_cost = 0
    
    def connect(self, component1: object, component2: object):
        """connects a component1 to component2"""
        if isinstance(component1, House):
            node1 = component1.node
            new_cable = node1.add_object(3)
            new_cable.modify_connection(component2)
            self.total_cable_cost += new_cable.cost
            if len(node1.cables) > 1:
                self.compare_cables(node1)  

    def connect_neighbours(self, component1: object, component2: object):
        """connects component 1 and 2 to eachother as neighbours"""
        component1.modify_connected_neighbours(component2, 0)
        component2.modify_connected_neighbours(component1, 0)
    
    def update_connections(self, component1: object, component2: object):
        for component in (component1, component2):
            if component.is_end_connected() == 1:
                if isinstance(component, House):
                    self.N_connected_houses += 1
                if isinstance(component, Battery):
                    self.N_connected_batteries += 1
    
    def compare_cables(self, node1: object):
        cables = node1.cables
        lowest_cost = 0
        for cable in cables:
            if lowest_cost == 0:
                lowest_cost = cable
            else:
                if lowest_cost.cost >= cable.cost:
                    node1.remove_object(lowest_cost)
                    lowest_cost = cable
                else:
                    node1.remove_object(cable)
    
    # MAGIC METHODS
    def __getitem__(self, coordinates):
        """allows the use of grid[x, y] to return the node at (x, y)"""
        return self.nodes[coordinates]

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

                            # add house object to node at (x, y)
                            self.nodes[x][y].add_object(1, capacity)
                            self.houses.append(self.nodes[x][y].house)
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])

                            # add battery object at (x, y)
                            self.nodes[x][y].add_object(2, capacity)
                            self.batteries.append(self.nodes[x][y].battery)

            self.N_houses = len(self.houses)
            self.N_batteries = len(self.batteries)
            
            # if data input successful 
            if nodes == self.N_houses + self.N_batteries:
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
                
                
                    
      
        
        