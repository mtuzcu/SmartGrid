# cable Object

class Cable:
    _counter = 0  # Class attribute to keep track of instances
    def __init__(self, cords1, cords2):
        """Node on grid containing node data"""
        self.cords1 = cords1  
        self.cords2 = cords2
        self._unique_id = Cable._counter
        Cable._counter += 1

    def __eq__(self, other):
        if isinstance(other, Cable):
            return self._unique_id == other._unique_id
        return False
    
    def __hash__(self):
        return hash(self._unique_id)
    
    def __repr__(self):
        return f"Cable({self.cords1}, {self.cords2})"
    



    #def __hash__(self):
    #    return hash(frozenset([self.cords1, self.cords2]))
    # def __eq__(self, other):
       # if self.cords1 in [other.cords1, other.cords2] and self.cords2 in [other.cords1, other.cords2]:
        #    return True


            if isinstance(house, House):
                cords = house.cords

            # lay cable
            x, y = self.cords
            while (x, y) != cords:
                if x != cords[0]:
                    x1 = functions.next_point(x, cords[0])
                    new_cable = classes.Cable((x, y), (x1, y))
                    x = x1
                elif y != cords[1]:
                    y1 = functions.next_point(y, cords[1])
                    new_cable = classes.Cable((x, y), (x, y1))
                    y = y1
                self.cables.add(new_cable)
            
            # update components
            if house != None:
                self.attach = house
                old_battery = self.battery
                house.connected.add(self)
                battery.update_chain(0)
                if old_battery != None:
                    old_battery.update()
            else:
                battery.connected.add(self)
                battery.houses.append(self)
                self.battery = battery
                self.attach = battery
                battery.connected.add(self)
            battery.update()
            return True
        return False