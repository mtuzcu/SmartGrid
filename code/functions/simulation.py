# Contains Functions for running the simulation
# Mahir Tuzcu - 11070978
import matplotlib.pyplot as plt

def district_solved(grid: object):
    """checks if the current district has all houses connected to a battery"""
    if grid.N_connected_houses == grid.N_houses:
        return 0
    return 1

def print_grid(grid: object):

    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#800080', '#FF00FF']

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

    # Place batteries on grid
    i = 0
    for battery in grid.batteries:
        (x, y) = battery.cords
        battery.distance = colors[i]
        ax.plot(x, y, 's', markersize=12, color=battery.distance, label='b' if 'b' not in [text.get_text() for text in ax.texts] else "")
        ax.text(x, y, int(battery.capacity), fontsize=10, ha='center', color='black')
        i += 1

    # Place houses on grid
    for house in grid.houses:
        (x, y) = house.cords
        ax.plot(x, y, '^', markersize=10, color=house.connections[2].distance, label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
        #if house.distance != float('inf'):
            #ax.text(x, y, int(house.distance), fontsize=12, ha='center', color='orange')

    # Place cables on grid
    for house in grid.houses:
        x0, y0 = house.cords
        x1, y1 = house.connections[0].cords
        ax.plot([x0, x1], [y0, y1], linewidth=1, color=house.connections[2].distance)

        #if battery.distance != float('inf'):
            #ax.text(x, y, int(battery.distance), fontsize=12, ha='center', color='orange')

    plt.show()
    return
