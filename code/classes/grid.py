# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import classes
import functions

cable_cost = 9

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []
        self.cables = set()

        # stats
        self.total_flow = 0
        self.total_capacity = 0
        self.total_output = 0
        self.total_cost = 0

    def store_solution(self, grid):
        """Copies the connections from seleted grid into the current grid"""
        for node in grid.houses:
            node1 = self[node]
            if node.connections[0] != node1.connections[0]:
                self.disconnect(node1, node1.connections[0])
                self.connect(node1, node.connections[0])

    def get_stats(self):
        self.total_cost = 0
        self.total_flow = 0
        for battery in self.batteries:
            self.total_cost += battery.cost
            self.total_flow += -(battery.max_capacity - battery.capacity)

    def solved(self):
        """test if current grid is solved and viable"""
        self.get_stats()
        for battery in self.batteries:
            if battery.capacity > 0:
                return False
        if round(self.total_flow) == round(self.total_output):
            return True
        return False
    
    def connect(self, component1, component2 = None): 
        cable = False
        if functions.legal_connection(component1, component2) == False:
            return False
        if isinstance(component1, (classes.House, classes.Battery)) and isinstance(component2, (classes.House, classes.Battery)):
            cable = classes.Cable(component1, component2)
        elif isinstance(component1, classes.Cable):
            cable = component1
            component1 = cable.node1
            component2 = cable.node2
        if cable != False:
            if cable not in component1.cables and cable not in component2.cables:
                component1.cables.add(cable)
                component2.cables.add(cable)
                self.cables.add(cable)
        return cable

    def disconnect(self, component1, component2 = None):  
        # remove connection referenced or connection connecting components
        cable = False
        if isinstance(component1, (classes.House, classes.Battery)) and isinstance(component2, (classes.House, classes.Battery)):
            cable = functions.find_cable(component1, component2)
        elif isinstance(component1, classes.Cable):
            cable = component1
            component1 = cable.node1
            component2 = cable.node2
        if cable != False:
            if cable in component1.cables and cable in component2.cables:
                component1.cables.remove(cable)
                component2.cables.remove(cable)
                self.cables.remove(cable)
        return cable
    
    def reset(self):
        self.total_cost = 0
        self.total_flow = 0
        self.cables = set()
        for battery in self.batteries:
            battery.reset()
        for house in self.houses:
            house.reset()

    # ==================================================================
    # Functions below are used to generate the grid. 
    # This is only used once at the start 
    # ==================================================================
        
    def create_grid(self, district_file_path):
        """generates a grid of nodes filed with houses and batteries according
        to the data given in csv_file."""

        # Get a list of all files in the directory
        file_list = os.listdir(district_file_path)  

        # Filter the list to include only CSV files
        csv_files = [file for file in file_list if file.endswith('.csv')]  

        if csv_files:
            nodes = 0
            # Iterate through each CSV file
            for csv_file in csv_files:
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
                            self.total_output += output
                            self.houses.append(classes.House((x, y), output))

                        # set node at (x, y) as battery
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])
                            self.total_capacity += capacity
                            self.batteries.append(classes.Battery((x, y), capacity, len(self.batteries)))
            
            # if data input successful 
            if nodes == len(self.houses) + len(self.batteries):
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
            
                
                    
      
        
        