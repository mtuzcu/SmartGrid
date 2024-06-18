# Contains Functions for running the simulation
# Mahir Tuzcu - 11070978
import matplotlib.pyplot as plt

def district_solved(grid: object):
    """checks if the current district has all houses connected to a battery"""
    if grid.N_connected_houses == grid.N_houses:
        return 0
    return 1

def print_grid(grid: object):

    deviate = 1
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-deviate, grid.size + deviate)
    ax.set_ylim(-deviate, grid.size + deviate)

    # Set layout of graph
    ax.set_xticks(range(0, grid.size + 1, 10))
    ax.set_yticks(range(0, grid.size + 1, 10))
    ax.set_xticks(range(0, grid.size + 1), minor=True)
    ax.set_yticks(range(0, grid.size + 1), minor=True)
    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.2)
    ax.grid(True)

    # Place houses on grid
    for house in grid.houses:
        (x, y) = house.cords
        ax.plot(x, y, '^', markersize=10, color='blue', label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
        #ax.text(x, y, fontsize=9, ha='center')
    
    # Place cables on grid
    for cable in grid.cables:
        x0, y0 = cable.connection1.cords
        x1, y1 = cable.connection2.cords
        ax.plot([x0, x1], [y0, y1], linewidth=1, color='black')

    # Place batteries on grid
    for battery in grid.batteries:
        (x, y) = battery.cords
        ax.plot(x, y, 's', markersize=10, color='red', label='b' if 'b' not in [text.get_text() for text in ax.texts] else "")
        ax.text(x, y, int(battery.property), fontsize=12, ha='center', color='orange')

    plt.show()
    return
