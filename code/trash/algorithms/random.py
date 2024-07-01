
import functions

class random:

    def __init__(self, grid) -> None:
        self.innitial(grid)

    def innitial(self, grid):

        for i in range(0, len(grid.houses) - 1):
            print(i)
            house = functions.get_random_component(grid.houses)
            while house.battery != None:
                house = functions.get_random_component(grid.houses)
            battery = functions.get_viable_batteries(grid, house)[0]
            house.connect(battery)

    def run(self, grid, iter = 1000):

        for i in range(0, iter):

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
    grid.connect(cable1)
    grid.connect(cable2)

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
                        if new_cable != old_cables[i]:
                            grid.connect(new_cable)
                            result2 = functions.analyse_network(nodes[i][j])
                            if result2 != False:
                                options.append((old_cables[i], new_cable, result1, result2))
                            grid.disconnect(new_cable) 
        grid.connect(old_cables[i])

    return options




    functions.print_grid(grid)
        