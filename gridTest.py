from grid import Grid
from road import Road, Junction, StopSign, TrafficLight, Roundabout, NullJunction

g = Grid(94, 46)
r = Road("Iodine Road", [ [4, 5], [4, 6], [4, 7], [4, 8] ])
r.classification = 3
r.numLanes = 6
r.speed = 50
r.toll = 1
g.roads.append(r)

s = Road("Bromine Road", [ [20, 8], [19, 8], [18, 8], [17, 8], [16, 7], [15, 7], [14, 8], [13, 8], [12, 8], [11, 8], [10, 8], [9, 8], [8, 8], [7, 8], [6, 8], [5, 8], [4, 8] ])
s.classification = 3
s.numLanes = 6
s.speed = 50
s.toll = 1
g.roads.append(s)

junctionRS = TrafficLight([r, s], [])
junctionRS.loc = [4, 8]
r.replaceJunction(junctionRS)
s.replaceJunction(junctionRS)


g.save("./data/roadNetwork.db")

#h = Grid(10, 10)
#h.reconstruct("./data/roadNetwork.db")
#for rd in h.roads:
#	print(rd.name + " " + str(rd.path) + " " + str(rd.junctions) + " " + str(rd.numLanes) + " " + str(rd.classification) + " " + str(rd.speed) + " " + str(rd.toll) + " " + str(rd.ID))
