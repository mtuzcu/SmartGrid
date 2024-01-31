
from classes.grid import *

if __name__ == "__main__":
   
    # inntialize a grid
    district = Grid()
    district.create_grid(51, 51)
    district.fill_grid('../districts/district_1')
    print(district)
    

    