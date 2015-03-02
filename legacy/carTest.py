from car import Car
from grid import Grid
from road import Road
from road import Junction

g = Grid(10, 10)

r = Road("Iodine Road", [ [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [1, 8], [2, 8], [3, 8], [4, 8] ])
r.classification = 1
r.numlanes = 2
r.speed = 35

#shorter path
#r2 = Road("Chlorine Road", [ [0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8] ])
#r2.classification = 1
#r2.numlanes = 2
#r2.speed = 35

#longer path, really fast speed and lots of lanes
r3 = Road("Bromine Road", [ [0, 0], [1, 1], [2, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [7, 8], [6, 8], [5, 8], [4, 8] ])
r3.classification = 1 #i forget the classifications
r3.numlanes = 8
r3.speed = 70

junction_1_3 = Junction(r, r3)
junction_1_3.loc = [0, 0]
r.replaceJunction([0, 0], junction_1_3)
r3.replaceJunction([0, 0], junction_1_3)

g.roads.append(r)
#g.roads.append(r2)
g.roads.append(r3)

c = Car([0, 0], [4, 8], [0, 0], g)
print("|" + str(c.currentRoad) + "|")
print(str(c.search(c.currentLocation, c.destination, c.currentRoad, [], 0, 0, [])))
  
#g.save("database.db")


