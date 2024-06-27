
# functions for algorithms to use
import functions
import copy
    
def viability(node):
    result = functions.scan_network(node)
    if result != False:
        battery = result[3]
        if battery.max_capacity + result[0] <= 0:
            return result
    return False

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

        # try double connection swap
        new_cable1 = grid.connect(nodes1[0], nodes2[i])
        new_cable2 = grid.connect(nodes1[1], nodes2[1 - i])

        # check result
        result1 = viability(nodes1[0])
        result2 = viability(nodes1[1])
        if result1 != False and result2 != False:
            options.append(((cable1, new_cable1, result1), (cable2, new_cable2, result2)))
        grid.disconnect(new_cable1)
        grid.disconnect(new_cable2)
    
    # restore original state
    grid.connect(cable1)
    grid.connect(cable2)

    # try single connection swaps
    nodes = [nodes1, nodes2]
    for i in range (0, 2):
        grid.disconnect(old_cables[i])
        for j in range(0, 2):
            result1 = viability(nodes[i][1 - j])
            if result1 != False:
                for k in range(0, 2):
                    new_cable = grid.connect(nodes1[j], nodes2[k])
                    result2 = viability(nodes[i][j])
                    if result2 != False:
                        options.append((old_cables[i], new_cable, result1, result2))
                    grid.disconnect(new_cable)   
        grid.connect(old_cables[i])

    return options

def pick_option(grid, options, mode = 'random'):
    if len(options) > 0:
        if mode == 'random': 
            option = functions.get_random_component(options)
        execute_change(grid, option)

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


            
            














# connect to different house



