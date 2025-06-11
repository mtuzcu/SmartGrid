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

    def run(self, grid, iter = 0):
        grid = self.generate_initial_solution(grid)
        lowest_cost_grid = copy.deepcopy(grid)
        lowest_cost = grid.total_cost
        steps = 0
        functions.intermediate_result(steps, lowest_cost, 0)

        i = 0
        d = 0 if iter == 0 else 1

        while i <= iter:
            i += d

            # mutate state
            functions.mutate(self.grid)
            self.grid.get_stats()
            current_cost = self.grid.total_cost

            if current_cost < lowest_cost:
                lowest_cost_grid = copy.deepcopy(grid)
                lowest_cost = current_cost
                steps += 1
                functions.intermediate_result(steps, lowest_cost, i)

        # return lowest cost grid found
        return lowest_cost_grid

if __name__ == "__main__":
    algorithms.main()
        