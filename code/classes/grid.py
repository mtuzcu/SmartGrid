# Contains Functions for generating grid layout using csv data
# Mahir Tuzcu - 11070978
import csv
import os
import classes
import functions
import copy

cable_cost = 9

class Grid:
    # Constructor method (initializer)
    def __init__(self):
        # dictionaires and lists
        self.houses: list = []
        self.batteries: list = []

        # stats
        self.total_flow = 0
        self.total_capacity = 0
        self.total_output = 0
        self.total_cost = 0

    def store_solution(self, grid):
        """Copies the connections from seleted grid into the current grid"""
        for battery1 in grid.batteries:
            battery0 = functions.get_equivalent(self, battery1)
            battery0.reset()
            battery0.cost = battery1.cost
            battery0.capacity - battery1.capacity
            for house in battery1.houses:
                house0 = functions.get_equivalent(self, house)
                house0.battery = battery0
                battery0.houses.append(house0)
            for cable1 in battery1.cables:
                cable0 = classes.Cable(functions.get_equivalent(self, cable1.node1), functions.get_equivalent(self, cable1.node2))
                battery0.cables.add(cable0)



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
    
    def connect(self, house, battery): 
        if house not in battery.houses:
            battery.houses.append(house)
            battery.capacity += house.output
            house.battery = battery


    def disconnect(self, house, battery):  
        # remove connection referenced or connection connecting components
        if house in battery.houses:
            battery.houses.remove(house)
            battery.capacity += - house.output
            house.battery = None
    
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
                            house = classes.House((x, y), output)
                            self.houses.append(house)

                        # set node at (x, y) as battery
                        else:
                            x, y = map(int, row[0].split(','))
                            capacity = float(row[1])
                            self.total_capacity += capacity
                            battery = classes.Battery((x, y), capacity, len(self.batteries))
                            self.batteries.append(battery)
 
            self.house_dict = {(house.cords): house for house in self.houses}
            self.battery_dict = {(battery.cords): battery for battery in self.batteries}
            # if data input successful 
            if nodes == len(self.houses) + len(self.batteries):
                print("grid successfully filled")
            else:
                print("Error occured during filling of grid. Not all data is filled")
            
                
                    
      
        
        