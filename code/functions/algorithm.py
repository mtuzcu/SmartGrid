
# functions for algorithms to use
import functions
import classes
import copy

def improvement(old, new):
    return new < old

def find_options(grid, cable1, cable2):

    # store current setup
    nodes1 = [cable1.node1, cable1.node2]
    nodes2 = [cable2.node1, cable2.node2]
    old_cables = [cable1, cable2]

    # try all possible new setups
    grid.disconnect(cable1)
    grid.disconnect(cable2)
    options = []

    # try double connection swap
    for i in range(0, 2):
        
        # check legality
        if functions.legal_connection(nodes1[0], nodes2[i]) == False or functions.legal_connection(nodes1[1], nodes2[1 - i]) == False:
            continue

        # create new cables
        new_cable1 = classes.Cable(nodes1[0], nodes2[i])
        new_cable2 = classes.Cable(nodes1[1], nodes2[1 - i])

        # check if new cables are unique from old cables
        if new_cable1 == cable1 or new_cable2 == cable2:
            continue

        # connect new cables
        grid.connect(new_cable1)
        grid.connect(new_cable2)

        # analyse result of new connections
        result1 = functions.analyse_network(nodes1[0])
        result2 = functions.analyse_network(nodes1[1])
        if result1 != False and result2 != False:
            options.append(((cable1, new_cable1, result1), (cable2, new_cable2, result2)))
        grid.disconnect(new_cable1)
        grid.disconnect(new_cable2)
    
    # restore original state
    grid.connect(old_cables[0])
    grid.connect(old_cables[1])

    # try single connection swaps
    nodes = [nodes1, nodes2]
    for i in range (0, 2):
        grid.disconnect(old_cables[i])
        for j in range(0, 2):
            result1 = None
            for k in range(0, 2):
                if functions.legal_connection(nodes1[j], nodes2[k]) == True:
                    if result1 == None:
                        result1 = functions.analyse_network(nodes[i][1 - j])
                    if result1 != False:

                        # check if new cable is not old cable
                        new_cable = classes.Cable(nodes1[j], nodes2[k])
                        new_cable = grid.connect(nodes1[j], nodes2[k])
                        result2 = functions.analyse_network(nodes[i][j])
                        if result2 != False:
                            options.append((old_cables[i], new_cable, result1, result2))
                        grid.disconnect(new_cable) 
        grid.connect(old_cables[i])

    return options

def pick_option(options, mode = 'random'):
    if len(options) > 0:
        if mode == 'random': 
            option = functions.get_random_component(options)
            return option
    return False

def execute_change(grid, option):
    # if option is a single cable change
    if len(option) == 4:
        grid.disconnect(option[0])
        grid.connect(option[1])
        battery1 = option[2][4]
        battery2 = option[3][4]
        if battery1 != battery2:
            battery1.apply_data(option[2])
        battery2.apply_data(option[3])

    # if option is a double cable change
    if len(option) == 2:
        if option[0][0] == option[0][1]:
            print(option[0][0], option[0][1])
            print(option[1][0], option[1][1])
        for change in option:
            grid.disconnect(change[0])
            grid.connect(change[1])
            battery = change[2][4]
            battery.apply_data(change[2])

def mutate(grid):
    cable1, cable2 = functions.get_random_cables(grid)
    options = find_options(grid, cable1, cable2)
    if len(options) > 0:
        option = pick_option(options)
        if option != False:
            execute_change(grid, option)
            return True

            
            














# connect to different house



