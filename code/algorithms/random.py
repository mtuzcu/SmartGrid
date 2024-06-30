
import functions
import random
import classes
import algorithms
import copy

class random:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.grid2 = copy.deepcopy(grid)
        self.random(self.grid)
        self.run()
    

    def random(self, grid):
        while grid.solved() == False:
            grid.reset()
            for i in range(0, len(grid.houses)):
                house = functions.get_random_component(grid.houses)
                while house.battery != None:
                    house = functions.get_random_component(grid.houses)
                viable_batteries = functions.get_viable_batteries(grid, house)
                if len(viable_batteries) == 0:
                    break
                battery = functions.get_random_component(viable_batteries)    
                grid.connect(house, battery)       

        for battery in grid.batteries:
            algorithms.prim_mst(battery.houses, grid)
        grid.get_stats()
        self.grid = grid

    def run(self, iter = 100):
        lowest_cost = 0
        for i in range(0, iter):
            print(i)
            self.grid.reset()
            self.random(self.grid)

            if lowest_cost == 0 or self.grid.total_cost < lowest_cost:
                lowest_cost = self.grid.total_cost
                self.grid2.store_solution(self.grid)
                print(lowest_cost)
        functions.print_grid(self.grid2)
    


        