
from classes.objects import *
import functions
from functions.simulation import * 
import algorithms

if __name__ == "__main__":
   
    # inntialize a grid
    district = Grid()
    district.create_grid(51, 51)
    district.fill_grid('../districts/district_1')
    hill = algorithms.hclimber(district)
    district = hill.run()
    print(district.total_cost)
    functions.print_grid(district)
    ax = False

    if ax == True:
        h1 = district.houses[0]
        h2 = district.houses[1]
        h3 = district.houses[2]
        b1 = district.batteries[0]
        b2 = district.batteries[1]

        district.connect(h3, h1)
        district.connect(h1, b1)
        district.connect(h2, b2)
        district.swap(h1, h3)

        print(h3, h3.connections[0], h3.connections[2])
        print(h2, h2.connections[0], h2.connections[2])
        print(h1, h1.connections[0], h1.connections[2])

  


    

    