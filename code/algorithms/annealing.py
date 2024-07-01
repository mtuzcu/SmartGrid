import algorithms
import copy
import functions
import math

class annealing:

    def __init__(self, grid, iter = 100) -> None:
        self.grid = grid
        self.neighbour = copy.deepcopy(self.grid)
        self.run(iter)

    def run(self, iter, T0 = 10000, alpha = 0.999):
          
        # get innitial solution
        random = algorithms.random()
        self.grid = random.generat_initial_solution(self.grid)
        self.neighbour = copy.deepcopy(self.grid)
        lowest_cost = self.grid.total_cost
        current_cost = lowest_cost

        i = 0
        # run algorithm
        while i < iter:
            i += 1

            # mutate state
            changes = functions.mutate(self.neighbour)
            self.neighbour.get_stats()
            delta = current_cost - self.neighbour.total_cost

            # if improvement is made or random chance requirement is met, store new grid
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_cost = self.neighbour.total_cost

                # if improvement is made over current best solution, store new best solution
                if current_cost < lowest_cost:
                    i = 0
                    self.grid = copy.deepcopy(self.neighbour)
                    lowest_cost = current_cost

            # if no improvement is state or annealing condition not met restore previous state
            else:
                functions.undo_changes(self.neighbour, changes)

            # temperature cooling
            T = T * alpha 