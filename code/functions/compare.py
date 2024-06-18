# contains functions to compare cables
# Mahir Tuzcu - 11070978

def filter_lowest_cost(node):
    """removes all cables except the lowest cost"""
    grid = node.grid
    cables = node.cables
    lowest_cost = 0
    for cable in cables:
        if lowest_cost == 0:
            lowest_cost = cable
        else:
            if lowest_cost.cost >= cable.cost:
                grid.disconnect(lowest_cost)
                lowest_cost = cable
            else:
                grid.disconnect(cable)

def remove_highest_cost(node):
    """removes the highest cost cable"""
    grid = node.grid
    cables = node.cables
    highest_cost = 0
    for cable in cables:
        if highest_cost == 0:
            highest_cost = cable
        else:
            if highest_cost.cost < cable.cost:
                highest_cost = cable
    grid.disconnect(highest_cost)