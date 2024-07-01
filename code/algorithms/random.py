import functions
import random
import algorithms
import copy

class random:

    def __init__(self) -> None:
        pass

    def generat_initial_solution(self, grid):
        while len(grid.unconnected_houses) > 0:
            house = functions.get_random_component(grid.unconnected_houses)
            functions.mutate(grid, house)

        for battery in grid.batteries:
            algorithms.optimal_network(battery)
        grid.get_stats()
        return grid

    def run(self, grid, iter):
        grid = self.generat_initial_solution(grid)
        lowest_cost_grid = copy.deepcopy(grid)
        lowest_cost = grid.total_cost
        for i in range(0, iter):

            # mutate state
            functions.mutate(self.grid)
            self.grid.get_stats()
            current_cost = self.grid.total_cost

            if current_cost < lowest_cost:
                lowest_cost_grid = copy.deepcopy(grid)
                lowest_cost = current_cost
        
        # return lowest cost grid found
        return lowest_cost_grid
    


        