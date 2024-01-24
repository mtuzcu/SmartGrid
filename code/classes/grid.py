# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import numpy as np

class Standard_Object:
        def __init__(self, x, y, max_property = 0) -> object:
            """Template for a standard grid object. Property depends on the object
            for houses and batteries it means remaining output/capacity. For cables it
            means 1 if cable is charged and 0 if not."""
            self.x_coordinate = x
            self.y_coordinate = y
            self.property
            self.max_property = max_property
            self.end_connections: list = []
            self.connected_neighbours: list = []
        
        def move_location(self, x, y):
            """Moves the object to the new x, y coordinate"""
            self.x_coordinate = x
            self.y_coordinate = y
        
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
        
        def modify_connected_neighbours(self, operation, connected_neighbour):
            """Adds or removes connected_neighbour to list of objects this object is connected to.
            use operation = 0 to add and 1 to remove the connected_neighbour."""
            if connected_neighbour not in self.connected_neighbours and operation == 0:
                self.end_connections.append(connected_neighbour)
            if connected_neighbour in self.connected_neighbours and operation == 1:
                self.end_connections.pop(connected_neighbour)
        
        def __hash__(self):
            # Assuming 'value' is immutable (e.g., an integer)
            return hash(self.value)

        def __eq__(self, other):
            # Custom equality comparison for instances of CustomKey
            return isinstance(other, CustomKey) and self.value == other.value

class House(Standard_Object):
    def __init__(self):
        """House objet containing data for instanced house. Only 1 house per node"""
     
class Battery(Standard_Object):
    def __init__(self):
        """Battery object containing data for instanced battery. Only 1 battery per node"""

class Cable(Standard_Object):
    def __init__(self):
        """cable object containing data for instanced cable. Multiple cables per node possible"""
    
class Node:
    def __init__(self, x, y):
        """Node on grid containing node data"""
        self.x_coordinate = x
        self.y_coordinate = y
        self.battery
        self.house
        self.cables = []
    
    def add_object(self, object_id, max_property = 0):
        """Adds a house or battery object if node not already occupied by said object
        object_id is 1 for a house and 2 for a battery and 3 for a cable dictionairy.
        If object_id refers to an already existing object, that object will be added."""
        if (object_id == 1 or isinstance(object_id, House)) and not self.house:
            if isinstance(object_id, House):
                self.house = object_id
            else:
                self.house = House(self.x_coordinate, self.y_coordinate, max_property)
        if (object_id == 2 or isinstance(object_id, Battery)) and not self.battery:
            if isinstance(object_id, Battery):
                self.battery = object_id
            else:
                self.battery = Battery(self.x_coordinate, self.y_coordinate, max_property)
        if (object_id == 3 or isinstance(object_id, Cable)):
            if isinstance(object_id, Cable):
                self.cables.append(object_id)
            else:
                self.cables.append(Cable(self.x_coordinate, self.y_coordinate, 1))
    
    def remove_object(self, object_id):
        """removes a house or battery object if node not already occupied by said object
        object_id is 0 to remove all objects, 1 for a house, 2 for a battery, 3 for a cable.
        if a cable object is reference is used for object_id, that specific cable will be 
        removed."""
        if isinstance(object_id, Cable):
            self.cables.pop(object_id)
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
        self.grid: dict
        self.houses: dict
        self.batteries: dict
        self.cables: dict
    
    def component_dictionairy(self, component: object, operation: int) -> dict:
        """If operation is 0, returns given component's dictionairy. If operation 
        is 1, returns batteries dictionairy if component is house and vice versa."""
    
        if isinstance(component, House):
            if operation == 0:
                return self.houses
            return self.batteries
        
        if isinstance(component, Battery):
            if operation == 0:
                return self.batteries
            return self.houses
        
    def connect_neighbours(self, component1: object, component2: object):
        """connects component 1 and 2 to eachother as neighbours"""
        component1.modify_connected_neighbours(component2, 0)
        component2.modify_connected_neighbours(component1, 0)
    
    def connect_end_components(self, component1: object, component2: object):
        """connects component 1 and 2 to eachother as end connections"""
        component1.modify_end_connection(0, component2)
        component2.modify_end_connection(0, component1)

    # ==================================================================
    # Functions below are used to generate the grid. 
    # This is only used once at the start 
    # ==================================================================

    def create_node(self, x, y) -> Node:
        """Creates a grid node"""
        return Node(x, y)
    
    def create_grid(self, size_x, size_y):
        """Creates a size_x by size_y grid of nodes"""
        self.grid.clear()
        self.houses.clear()
        self.batteries.clear()
        for x in range(0, size_x):
            for y in range(0, size_y):
                self.grid[(x, y)] = self.create_node(x, y)
    
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
                            self.grid[(x, y)].add_object(1, capacity)
                            self.houses[(x, y)] = self.grid[(x, y)].house
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])

                            # add battery object at (x, y)
                            self.grid[(x, y)].add_object(2, capacity)
                            self.batteries[(x, y)] = self.grid[(x, y)].battery

            # if data input successful 
            if nodes == len(self.houses) + len(self.batteries):
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
                
                
                    
      
        
        