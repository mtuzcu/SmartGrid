
# functions for algorithms to use
import functions
import classes
import copy

def find_options(cable1, cable2):
    
    # find composition of nodes
    comp, n = functions.get_structure(cable1, cable2)
    if comp[0] == [0, 1]:
        nodes1 = [cable1.node1, cable1.node2]
    else:
        nodes1 = [cable1.node2, cable1.node1]
    if comp[1] == [0, 1]:
        nodes2 = [cable2.node1, cable2.node2]
    else:
        nodes2 = [cable2.node2, cable2.node1]
    if comp == [0, 0]:
        return False
    options = []

    # for 3 body case
    cable00 = classes.Cable(nodes1[0], nodes2[0])
    options = functions.legal_option(options, ([cable00], [cable1]))
    options = functions.legal_option(options, ([cable00], [cable2]))
    cabs = [cable00]
    # for 4 body cases:
    if n == 4:
        cable101 = classes.Cable(nodes1[0], nodes2[1])
        cable201 = classes.Cable(nodes2[0], nodes1[1])
        options.append(([cable101, cable201], [cable1, cable2]))
        options.append(([cable101], [cable1]))
        options.append(([cable201], [cable2]))
        
    yoa = 0
    if yoa == 1:

        for cable in cabs:
            if cable.node1 == cable.node2:
                print(cable)
                print(cable1, cable2)
                print(nodes1, nodes2)
                print(comp)
                print(cable2.node1.cables)
                print(cable2.node2.cables)
    return options

def pick_option(options, mode = 'random'):
    if len(options) > 0:
        if mode == 'random': 
            option = functions.get_random_component(options)
            return option
    return False

def execute_change(grid, option):
    start = len(grid.cables)
    cost = grid.total_cost
    for cable in option[1]:
        grid.disconnect(cable)
    for cable in option[0]:
        grid.connect(cable)
    grid.update()
    if grid.solved() == True and start == len(grid.cables):
        return grid.total_cost - cost
    
    # if change not viable, return original state
    else:
        for cable in option[0]:
            grid.disconnect(cable)
        for cable in option[1]:
            grid.connect(cable)
        grid.update()
        grid.solved()
    return False

def mutatee(grid):
    cable1, cable2 = functions.get_random_cables(grid)
    options = find_options(cable1, cable2)
    print('##########')
    while len(options) > 0:
        option = pick_option(options)
        print('----')
        if (delta := execute_change(grid, option)) == False:
            options.remove(option)
        else:
            print(option)
            return delta
    return False

def mutate(grid):
    cable1, cable2 = functions.get_random_cables(grid)
    options = find_options(cable1, cable2)
    if options != False:
        if len(options) > 0:
            option = pick_option(options)
            if (delta := execute_change(grid, option)) == False:
                return False
            else:
                return delta

            
            














# connect to different house



