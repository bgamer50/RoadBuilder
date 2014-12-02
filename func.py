##__Begin Method Definitions__##
def shash(n):
	return hash(str(n))
def cleanZones(g):
    k = 0
    while k < len(g.zones):
      if len(g.zones[k]) == 0:
		try:
			g.zones.pop(k)
		except:
			pass
      k += 1

def getNeighbors(loc, g):
 	for n in g.nodes:
 		if n.x == loc[0] and n.y == loc[1]:
 			return n.neighbors
 	print("Error: No neighbors for loc " + str(loc))
 	return []
##__End Method Definitions__##

##__Begin Class Definitions__##
class fakeObject:
	list = []
##__End Class Definitions__##