from gridPrime import Grid
from func import getNeighbors
class Car:
	points = 180 #the number of points this car has.  Moves when this gets to 0.  i.e. speed limit 20 -> 6 ticks
	location = [] #the current location of this car (corresponds to an x and y)
	destination = [] #the car's intended destination
	path = [] #the locations this car intends to travel to, in order.
	myGrid = None #the grid that contains ths car.
	MAX_RECUSION_DEPTH = 100 #the maximum depth of recursion for the search algorithm
	previousDirection = 0 #last direction the car was moving in

	def __init__(self, g, x, y, destX, destY): #grid, current location, destination
		self.points = 180
		self.location = [x, y]
		self.path = []
		self.destination = [destX, destY]
		self.myGrid = g

	def search(self):
		self.path = self.searchRecursive([[self.location], 0], self.location)[0]

	def getQualityIndex(self, r):
		#a weight that favors roads with high speeds and many lanes.
		#print(str(r.numLanes) + " " + str(r.speed))
		return pow(r.numLanes * r.speed, -1)

	def minP(self, pArray):
		#returns the best path
		if len(pArray) == 0:
			return [None, 99999999999]
		bestP = pArray[0]
		for p in pArray:
			if p[1] < bestP[1]:
				bestP = p
		return bestP

	def containsLocation(self, p, x, y):
		for n in p:
			if n[0] == x and n[1] == y:
				return 1
		return 0

	def sameLocation(self, l1, l2):
		if l1[0] == l2[0] and l1[1] == l2[1]:
			return 1
		return 0

	def searchRecursive(self, p, loc):
		#base case, when it has reached max recursion depth
		if len(p[0]) >= 100:
			return [None, 9999999999]

		#second base case, when it has found the destination
		if self.sameLocation(loc, self.destination):
			weight = p.pop()
			return p + [self.destination, weight]

		#recurs to each neighbor
		nbrs = getNeighbors(loc, self.myGrid)
		newPArray = []
		for n in nbrs:
			if not self.containsLocation(p[0], n[0], n[1]):
				tempP = [p[0] + [[n[0], n[1]]], p[1] + self.getQualityIndex(n[2])] #first array element is the path, second is the weight
				newPArray.append(self.searchRecursive(tempP, [n[0], n[1]]))
		#returns minimum
		return self.minP(newPArray)

	def currentRoad(self):
		for n in self.myGrid.nodes:
			if n.x == self.location[0] and n.y == self.location[1] and len(n.neighbors) > 0:
				return n.neighbors[0][2]
			else:
				return None

	def direction(self):
		#0 - moving left to right; 1 - moving right to left; 2 - moving bottom to top; 3 = moving top to bottom
		try:
			dx = self.path[1][0] - self.location[0]
			dy = self.path[1][0] - self.location[1]
		except:
			return self.previousDirection
		if dx > 0 and dy == 0:
			self.previousDirection = 0
			return 0
		elif dx < 0 and dy == 0:
			self.previousDirection = 1
			return 1
		elif dy > 0 and dx == 0:
			self.previousDirection = 2
			return 2
		elif dy < 0 and dx == 0:
			self.previousDirection = 3
			return 3
		else:
			if dx > 0:
				return 0
			if dx < 0:
				return 1