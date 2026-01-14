# Contains the standard algoritms 
# Mahir Tuzcu - 11070978 

import functions


# Generate initial solution
def innitial(grid):
    houses = grid.houses
    for house in houses:
        battery = functions.get_viable_batteries(house)[0]
        grid.connect(house, battery)
    return grid

def proxy_solution(grid):
      for battery in grid.batteries:
          battery.distances = functions.get_distances(battery, 1)
      for i in range(1, len(grid.houses)):
            for battery in grid.batteries:
                house = battery.distances[i]
                if functions.viability(house, battery):
                    if house.connections[0] == None:
                        grid.connect(house, battery)
                    elif functions.improvement(house, battery):
                        grid.disconnect(house, house.connections[0])
                        grid.connect(house, battery)

def untangle(grid):
    hlist = functions.longest_connections(grid)
    for i in range(0, len(hlist)):
        house1 = hlist[len(hlist) - i - 1]
        for house2 in grid.houses:
            if house1.connections[2] != house2.connections[2] and house1.connections[0] != house1.connections[2]:
                if functions.improvement(house1, house2):
                    grid.disconnect(house1, house1.connections[0])
                    grid.connect(house1, house2)


    

    










def testo(district):
    h = district.houses[0]
    h2 = district.houses[1]
    h3 = district.houses[2]
    h4 = district.houses[3]
    h5 = district.houses[4]
    b = district.batteries[0]
  
    district.connect(h, b)
    district.connect(h2, h)
    district.connect(h3, h2)
    district.disconnect(h, b)
    district.connect(h2,b)
    print('-----')

    print(h, h.capacity, h.output, h.connections)
    print(h2, h2.capacity, h2.output, h2.connections)
    print(h3, h3.capacity, h3.output, h3.connections)
    print(b, b.capacity, b.output, b.connections)




    


