
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




    functions.print_grid(grid)
        