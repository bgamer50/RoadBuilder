from gridPrime import Grid
from func import getNeighbors
class Car:
	points = 180 #the number of points this car has.  Moves when this gets to 0.  i.e. speed limit 20 -> 6 ticks
	location = None #the current location of this car (corresponds to a node)
	destination = [] #the car's intended destination
	path = [] #the locations this car intends to travel to, in order.
	myGrid = None #the grid that contains ths car.
	MAX_RECUSION_DEPTH = 100 #the maximum depth of recursion for the search algorithm

	def __init__(self, g, loc, dest): #grid, current location, destination
		self.points = 180
		self.location = loc
		self.myGrid = g

	def search(self):
		path = searchRecursive([location, 0], location)

	def getQualityIndex(self, r):
		#a weight that favors roads with high speeds and many lanes.
		#print(str(r.numLanes) + " " + str(r.speed))
		return pow(r.numLanes * r.speed, -1)

	def minP(pArray):
		#returns the best path
		bestP = pArray[0]
		for p in pArray:
			if p[1] < bestP[1]:
				bestP = p
		return bestP

	def containsLocation(p, x, y):
		for n in p:
			if n[0] == x and n[1] == y:
				return 1
		return 0

	def searchRecursive(self, p, loc):
		#base case, when it has reached max recursion depth
		if len(p[0]) >= 100:
			return [None, 9999999999]

		#second base case, when it has found the destination
		if sameLocation(loc, self.destination):
			return [destination, 0]

		#recurs to each neighbor
		nbrs = getNeighbors(loc)
		newPArray = []
		for n in nbrs:
			if not containsLocation(p, n[0], n[1]):
				tempP = [p[0] + [n[0], n[1]], p[1] + getQualityIndex(n[2])]
				newPArray.append(self.searchRecursive(tempP, [n[0], n[1]]))
		#returns minimum
		return minP(newPArray)