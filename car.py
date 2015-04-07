from grid import Grid
class Car:
	points = 180 #the number of points this car has.  Moves when this gets to 0.  i.e. speed limit 20 -> 6 ticks
	location = [] #the current location of this car (corresponds to a node)
	destination = [] #the car's intended destination
	path = [] #the locations this car intends to travel to, in order.
	myGrid = None #the grid that contains ths car.
	MAX_RECUSION_DEPTH = 100 #the maximum depth of recursion for the search algorithm
	previousDirection = 0 #last direction the car was moving in

	def __init__(self, g, x, y, destX, destY): #grid, current location, destination
		self.points = 180
		self.path = []
		self.destination = [destX, destY]
		self.myGrid = g
		self.location = self.myGrid.getNode(x, y)

	def search(self):
		p = self.searchRecursive([0, [self.myGrid.getNode(self.location.x, self.location.y)]], self.destination)
		p = p[1]
		if p == None:
			self.path = []
		else:
			self.path = p

	def getQualityIndex(self, r):
		#a weight that favors roads with high speeds and many lanes.
		return pow(r.numLanes * r.speed, -1)

	def minP(self, pArray):
		#returns the best path
		if len(pArray) == 0:
			return [99999999999, [None]]
		bestP = pArray[0]
		for p in pArray:
			if p[1] < bestP[1] and len(p[0]) >= 1:
				bestP = p
		return bestP

	def containsLocation(self, p, nd):
		for n in p:
			if n.x == nd.x and n.y == nd.y:
				return 1
		return 0

	def sameLocation(self, l1, l2):
		if l1[0] == l2[0] and l1[1] == l2[1]:
			return 1
		return 0

	def searchRecursive(self, p, destination):
		#base case, when it has reached max recursion depth
		if len(p[1]) >= 100:
			return [9999999999, [None]]

		#second base case, when it has found the destination
		nd = p[1][len(p[1]) - 1]
		if self.sameLocation([nd.x, nd.y], self.destination):
			return p

		#recurs to each neighbor
		#nbrs = self.myGrid.getNeighbors(nd)
		newPArray = []
		for nbr in nd.neighbors:
			nodeNbr = self.myGrid.getNode(nbr[0], nbr[1])
			if not self.containsLocation(p[1], nodeNbr):
				tempP = []
				tempP.append(p[0] + self.getQualityIndex(nbr[2]))
				tempP.append(p[1] + [nodeNbr])
				newPArray.append(self.searchRecursive(tempP, destination))
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