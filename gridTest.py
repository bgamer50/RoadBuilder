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
n.neighbors.append( [2, 1, r] )

n1 = Node(2, 1)
n1.neighbors.append( [3, 1, r] )
n1.neighbors.append( [1, 0, r] )

n2 = Node(3, 1)
n2.neighbors.append( [2, 1, r] )
n2.neighbors.append( [4, 0, r] )

n3 = Node(4, 0)
n3.neighbors.append( [3, 1, r] )

n4 = Node(25, 25)
n4.zone = 1

g.nodes.append(n)
g.nodes.append(n1)
g.nodes.append(n2)
g.nodes.append(n3)
g.nodes.append(n4)

g.save("./data/roadNetwork.db")

g2 = Grid(94, 46)
g2.load("./data/roadNetwork.db")

print(g2.nodes)