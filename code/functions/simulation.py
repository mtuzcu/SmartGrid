# Contains Functions for running the simulation
# Mahir Tuzcu - 11070978
import matplotlib.pyplot as plt
import classes

def district_solved(grid: object):
    """checks if the current district has all houses connected to a battery"""
    if grid.N_connected_houses == grid.N_houses:
        return 0
    return 1

def print_grid(grid: object):

    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFA500', '#800080', '#FF00FF']

    grid.size = 50
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

    placed_houses = set()
    placed_cables = set()

    # Place batteries on grid
    for battery in grid.batteries:
        network_color = colors[battery.id]
        (x, y) = battery.cords
        ax.plot(x, y, 's', markersize=12, color=network_color, label='b' if 'b' not in [text.get_text() for text in ax.texts] else "")
        ax.text(x, y, int(battery.capacity), fontsize=10, ha='center', color='black')

        # place houses on grid:
        for house in battery.houses:
            placed_houses.add(house)
            (x, y) = house.cords
            ax.plot(x, y, '^', markersize=10, color=network_color, label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
    
        # place cables
        for cable in battery.cables:
            network_color = colors[battery.id]
            x0, y0 = cable.node1.cords
            x1, y1 = cable.node2.cords
            d = 0
            ax.plot([x0, x1], [y0 + d, y1 + d], linewidth=1, color=network_color)

    # place unconnected houses on grid:
        for house in grid.houses:
            if house not in placed_houses:
                (x, y) = house.cords
                ax.plot(x, y, '^', markersize=10, color='black', label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
   
    plt.show()
    return
