
import algorithms.hillclimber
import classes
import functions
import algorithms
import cProfile
import time


def main():

    # inntialize a grid
    grid = classes.Grid()
    #grid.create_grid('../districts/district_1')
    grid.create_grid('../districts/district_1')  
    random = algorithms.random()
    random.random(grid)
    functions.print_grid(grid)
    #algorithms.hillclimber(grid)x
    
if __name__ == "__main__":
    cProfile.run('main()', 'profile_output.prof')

    

    