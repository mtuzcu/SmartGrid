import algorithms
import copy
import functions

class hillclimber:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.neighbour = copy.deepcopy(self.grid)
        self.run(iter)

    def run(self, iter):
          
        # get innitial solution
        random = algorithms.random()
        self.grid = random.generat_initial_solution(self.grid)
        self.neighbour = copy.deepcopy(self.grid)
        lowest_cost = self.grid.total_cost

        i = 0
        # run algorithm
        while i < iter:
            i += 1

            # mutate state
            changes = functions.mutate(self.neighbour)
            self.neighbour.get_stats()
            current_cost = self.neighbour.total_cost

            # store new state if improvement is made
            if current_cost < lowest_cost:
                i = 0

                #self.grid.store_solution(self.neighbour)
                self.grid = copy.deepcopy(self.neighbour)
                lowest_cost = current_cost

            # if no improvement is made, restore previous state
            else:
                functions.undo_changes(self.neighbour, changes)
            
        

