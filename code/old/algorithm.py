
# functions for algorithms to use
import functions
import classes
import copy

def find_options(cable1, cable2):
    
    # find composition of nodes
    n = functions.n_nodes(cable1, cable2)
    nodes1 = [cable1.node1, cable1.node2]
    nodes2 = [cable2.node1, cable2.node2]
    new_cables = []

    

    return new_cables
   

def pick_option(options, mode = 'random'):
    if len(options) > 0:
        if mode == 'random': 
            option = functions.get_random_component(options)
            return option
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
    new_cables = find_options(cable1, cable2)
    #print(new_cables)
    if len(new_cables) > 0:
        d = execute_change(grid, [cable1, cable2], new_cables)
        print(d)

       # if (delta := execute_change(grid, option)) == False:
            #return False
       # else:
     




def exexcute_change(grid, option):
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

            














# connect to different house



