# Contains Functions for running the simulation
# Mahir Tuzcu - 11070978

def district_solved(grid: object):
    """checks if the current district has all houses connected to a battery"""
    if grid.N_connected_houses == grid.N_houses:
        return 0
    return 1