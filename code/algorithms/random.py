
import functions
import random
import classes
import algorithms

class random:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.innitial(self.grid)
        #self.run(self.grid)
        algorithms.prsm_mst(grid.batteries[0].network)
        functions.print_grid(self.grid)

    def innitial(self, grid):
        while grid.solved() == False:
            grid.reset()
            for i in range(0, len(grid.houses)):
                house = functions.get_random_component(grid.houses)
                while len(house.cables) > 0:
                    house = functions.get_random_component(grid.houses)
                viable_batteries = functions.get_viable_batteries(grid, house)
                if len(viable_batteries) == 0:
                    break
                battery = functions.get_random_component(viable_batteries)    
                grid.connect(house, battery)     
                battery.update()    

        self.grid = grid
        print(grid.solved())

    def run(self, grid, iter = 100):
        lowest_cost = 0
        print(len(grid.cables))
        for i in range(0, iter):
            #functions.mutate(grid)

            if lowest_cost == 0 or grid.total_cost < lowest_cost:
                lowest_cost = grid.total_cost
                print(lowest_cost)


        