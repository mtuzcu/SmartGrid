#
import functions
import algorithms
import classes
import copy

def get_viable_batteries(grid, house) -> list:
    """returns a list of all battery nodes that can accomodate house"""
    return [battery for battery in grid.batteries if battery.viability(house)]

def get_viable_houses(house, battery) -> list:
    """returns a list of all battery nodes that can accomodate house"""
    viable_houses = [house2 for house2 in battery.houses if viability(house, house2)]
    return viable_houses if viable_houses else False

def viability(house1, house2):
    if isinstance(house1, classes.Battery) or isinstance(house2, classes.Battery):
        return False
    
    capacity1 = house1.battery.capacity - house1.output + house2.output if house1.battery else 0
    capacity2 = house2.battery.capacity - house2.output + house1.output if house2.battery else 0

    return capacity1 <= 0 and capacity2 <= 0
        

def get_options(grid, house, mode = 'random'):

    options = None            
    viable_batteries = get_viable_batteries(grid, house)
    if len(viable_batteries) > 0:
        battery = functions.get_random_component(viable_batteries)
        return [(house, battery, house.battery)]
    else:
        battery_queue = copy.copy(grid.batteries)
        house2 = None
        while house2 == None and len(battery_queue) > 0: 
            battery = functions.get_random_component(grid.batteries)
            viable_houses = get_viable_houses(house, battery)
            if viable_houses != False:
                house2 = functions.get_random_component(viable_houses)
                options = [(house, house2.battery, house.battery), (house2, house.battery, house2.battery)]
    return options

def apply_option(grid, options):
    for pair in options:
        grid.connect(pair[0], pair[1])

def undo_changes(grid, options):
    for pair in options:
        grid.connect(pair[0], pair[2])
    update_batteries(options, 1)
    
def mutate(grid, house = None):
    if house == None:
        house = functions.get_random_component(grid.houses)
    options = get_options(grid, house)
    if options != None:
        apply_option(grid, options)
        functions.update_batteries(options)
        return options
    return None

def update_batteries(options, mode = 0):
    updated = set()
    for pair in options:
        for i in [1, 2]:
            if pair[i] != None and pair[i] not in updated:
                updated.add(pair[i])
                if mode == 0:
                    pair[i].previous_connections = copy.copy(pair[i].connections)
                    pair[i].previous_cost = pair[i].cost
                    algorithms.optimal_network(pair[i])
                else:
                    pair[i].connections = pair[i].previous_connections
                    pair[i].cost = pair[i].previous_cost
      
    
