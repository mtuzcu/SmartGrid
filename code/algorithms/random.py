import functions
import algorithms
import copy

class random:
    def __init__(self) -> None:
        pass

    def generate_initial_solution(self, grid):
        while len(grid.unconnected_houses) > 0:
            house = functions.get_random_component(grid.unconnected_houses)
            functions.mutate(grid, house)

        for battery in grid.batteries:
            algorithms.optimal_network(battery)
        grid.get_stats()
        return grid

    def step(self, grid):
     
        # mutate state
        functions.mutate(self.grid)
        self.grid.get_stats()
        current_cost = self.grid.total_cost

        # new lower-cost sulation found
        if current_cost < lowest_cost:
            lowest_cost_grid = copy.deepcopy(grid)
            lowest_cost = current_cost
            return 0, lowest_cost_grid

        # No new lower-cost solution has been found
        return 1

        