from gridPrime import Grid
from road import Road
from node import Node

g = Grid(94, 46)

r = Road("Fluorine Road", [[]])
r.classification = 3
r.numLanes = 6
r.speed = 55
r.toll = 0
g.roads.append(r)

n = Node(1, 0)
n.neighbors.append( [1, 1, r] )
n.zone = 2
g.nodes.append(n)

g.save("./data/roadNetwork.db")

g2 = Grid(94, 46)
g2.load("./data/roadNetwork.db")

print(g2.nodes)