
from classes.grid import *
from functions.distance import *
from functions.operators import *
from functions.simulation import * 
from algorithms.general import *
from algorithms.universal import *

if __name__ == "__main__":
   
    # inntialize a grid
    district = Grid()
    district.create_grid(51, 51)
    district.fill_grid('../districts/district_1')
    executor = algorithm_executor(district)
    district = executor.run_algorithm()
    print(district.total_cable_cost)
    print_grid(district)

    

    