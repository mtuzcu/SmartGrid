
import classes
import functions
import algorithms

if __name__ == "__main__":
   
    # inntialize a grid
    grid = classes.Grid()
    #grid.create_grid('../districts/district_1')
    grid.create_grid('../districts/district_1')
    algorithms.random(grid)

    yo = 0
    if yo == 1:

        h = grid.houses[0]
        h2 = grid.houses[1]
        h3 = grid.houses[2]
        h4 = grid.houses[3]
        h5 = grid.houses[4]
        b = grid.batteries[0]
    
        c1 = grid.connect(h, h2)
        grid.connect(h, b)
        print(b, h, h2)
        #grid.connect(h3, b)

        print(functions.scan_path(h2, h)[0])


  


    

    