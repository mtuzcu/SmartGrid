# Contains Functions for running the simulation
# Mahir Tuzcu - 11070978
import matplotlib.pyplot as plt
import classes

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
    offset = 0.11
    i = 0

    # Place batteries on grid
    for battery in grid.batteries:
        network_color = colors[i]
        (x, y) = battery.cords
        ax.plot(x, y, 's', markersize=12, color=network_color, label='b' if 'b' not in [text.get_text() for text in ax.texts] else "")
        ax.text(x, y, int(battery.capacity), fontsize=10, ha='center', color='black')

        # place houses on grid:
        for house in battery.houses:
            if isinstance(house, classes.House):
                placed_houses.add(house)
                (x, y) = house.cords
                ax.plot(x, y, '^', markersize=10, color=network_color, label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
        
        for connection in battery.connections:
            start, mid, end = connection
            if mid == None:
                 start, end = calculate_offset((start, end), offset, i)
                 ax.plot([start[0], end[0]], [start[1], end[1]], color=network_color, linewidth=1)
            else:
                start, mid, end = calculate_offset((start, mid, end), offset, i, 1)
                ax.plot([start[0], mid[0]], [start[1], mid[1]], color=network_color, linewidth=1)
                ax.plot([mid[0], end[0]], [mid[1], end[1]], color=network_color, linewidth=1)
        i += 1

    # place unconnected houses on grid:
        for house in grid.houses:
            if house not in placed_houses:
                (x, y) = house.cords
                ax.plot(x, y, '^', markersize=10, color='black', label='a' if 'a' not in [text.get_text() for text in ax.texts] else "")
   
    plt.show()
    return


def calculate_offset(line, offset, network_number, mode = 0):
    sign = (-1)**network_number
    offset_factor = (network_number + 1) // 2

    if mode == 0:
        (x1, y1), (x2, y2) = line
        if offset_factor > 0:
            if x1 == x2:
                y1 += sign * offset_factor * offset
                y2 += sign * offset_factor * offset
            else:
                x1 += sign * offset_factor * offset
                x2 += sign * offset_factor * offset
        return (x1, y1), (x2, y2)

    if mode == 1:
        (x1, y1), (x2, y2), (x3, y3) = line
        if offset_factor > 0:
            if y1 == y2:
                y1 += -sign * offset_factor * offset
                y2 += -sign * offset_factor * offset
                x2 += sign * offset_factor * offset
                x3 += sign * offset_factor * offset

            if x1 == x2:
                x1 += sign * offset_factor * offset
                x2 += sign * offset_factor * offset
                y2 += -sign * offset_factor * offset
                y3 += -sign * offset_factor * offset

        return (x1, y1), (x2, y2), (x3, y3)
