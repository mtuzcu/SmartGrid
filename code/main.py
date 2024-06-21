
from classes.grid import *
import functions
from functions.simulation import * 
import algorithms

if __name__ == "__main__":
   
    # inntialize a grid
    district = Grid()
    district.create_grid(51, 51)
    district.fill_grid('../districts/district_1')
    #executor = algorithm_executor(district)
    #district = executor.run_algorithm()
    hill = algorithms.annealing(district)
    district = hill.simulated_annealing(300000)
    algorithms.cleanup(district)
    print(district.total_cost)
    functions.print_grid(district)


  


    

    