from grid import Grid
from road import Road
from road import Junction
from func import shash
from copy import copy
#hopefully i'll add in trucks and accidents that extend Car.
class Car:
	homeLocation = [] #grid square
	destination = [] #this can be modified, helps save memory
	currentLocation = []
	previousLocation = []
	path = []
	currentRoad = None
	destinationRoad = None
	homeRoad = None
	myGrid = None
	
	def getQualityIndex(self, r):
		#a weight that favors roads with high speeds and many lanes.
		#print(str(r.numLanes) + " " + str(r.speed))
		return pow(r.numLanes * r.speed, -1)
	
	def mutateQualityIndex(self, r, qi):
		#takes the quality index and plays around with it.
		#10% chance of the index of a freeway being multiplied by 10.
		if r.classification == 4 or r.classification == 5:
			return 10 * qi
	
	def search(self, l, d, rd, pointArray, weight, depth, visited):
		if(rd == None):
			print("Error: Current Road is Null.")
			exit()
		#print(str(pointArray) + " " + str(weight) + " " + str(depth))

		if depth > 800 or l in visited:
			return [10000000000, pointArray]
		
		if shash(l) == shash(d):
			return [weight, pointArray]
		#every l, unless it's at a junction, has only 2 neighbors.
		#we start by checking to see if l is at a junction.
		junction = 0
		try:
			if shash(l) == shash(rd.path[0]) or shash(l) == shash(rd.path[len(rd.path) - 1]):
				junction = 1
			if junction != 1:
				visited.append(l)
				pa1 = copy(pointArray)
				l1 = rd.path[rd.path.index(l) + 1]
				pa1.append(l1)
				s1 = self.search(l1, d, rd, pa1, weight + self.getQualityIndex(rd), depth + 1, visited)
	
				pa2 = copy(pointArray)
				l2 = rd.path[rd.path.index(l) - 1]
				pa2.append(l2)
				s2 = self.search(l2, d, rd, pa2, weight + self.getQualityIndex(rd), depth + 1, visited)

				if s1[0] < s2[0]:
					return s1
				else:
					return s2
			else:
				visited.append(l)
				searches = []
				j = rd.getJunction(l)
				for r in j.roads:
					indexInR = r.path.index(l)
					pacopy = copy(pointArray)
					if indexInR == 0:
						newL = r.path[indexInR + 1]
						pacopy.append(newL)
						searches.append( self.search(newL, d, r, pacopy, weight + self.getQualityIndex(r), depth + 1, visited) )
					else:
						newL = r.path[indexInR - 1]
						pacopy.append(newL)
						searches.append( self.search(newL, d, r, pacopy, weight + self.getQualityIndex(r), depth + 1, visited) )
				minimum = [1000000000000000, pointArray]
				for s in searches:
					if s[0] < minimum[0]:
						minimum = s
				return minimum
		except:
			visited.append(l)
			if(rd.path.index(l) == 0):
				pa1 = copy(pointArray)
				l1 = rd.path[rd.path.index(l) + 1]
				pa1.append(l1)
				return self.search(l1, d, rd, pa1, weight + self.getQualityIndex(rd), depth + 1, visited)
			else:
				pa1 = copy(pointArray)
				l1 = rd.path[rd.path.index(l) - 1]
				pa1.append(l1)
				return self.search(l1, d, rd, pa1, weight + self.getQualityIndex(rd), depth + 1, visited)
				
	def updatePosition(self):
		for rd in self.myGrid.roads:
			for j in rd.junctions:
				if shash(self.currentLocation) == shash(j.loc):
					for r in j.roads:
						for l in r.path:
							if shash(self.path[1]) == shash(l):
								self.currentRoad = r
								break		
		self.currentLocation = self.path[1]
		self.path = self.path[1:]

	def __init__(self, home, dest, curLoc, g):
		self.homeLocation = home
		self.destination = dest
		self.currentLocation = curLoc
		self.myGrid = g
		for r in self.myGrid.roads:
			if self.currentLocation in r.path:
				self.currentRoad = r
				break
		for r in self.myGrid.roads:
			if self.homeLocation in r.path:
				self.homeRoad = r
				break
		for r in self.myGrid.roads:
			if self.destination in r.path:
				self.destinationRoad = r
		#self.path = search(self.currentLocation, self.destination, self.currentRoad, [], 0, 0, [])


