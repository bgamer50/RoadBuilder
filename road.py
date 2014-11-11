from func import shash
from copy import deepcopy as copy

#This is the Road class, responsible for holding all road information.  Ultimately, the most important info is its path and junctions.
class Road:
    path = [] #List of each place on the grid it passes through. WILL BE REMOVED
    #the path's start and end are junctions.
    junctions = [] #constant length of 2 WILL BE REMOVED
    numLanes = 2 #default is a 2-lane road
    classification = 1 #See below
    speed = 25
    toll = 0
    name = ""
    ID = None
        
    def __init__(self, n, points): #POINTS MUST BE IN ORDER!!!!!
        self.name = n
	self.path = points
	self.junctions = []

	j = NullJunction(self)
	j.loc = points[0]
	self.junctions.append(j)

	k = NullJunction(self)
	k.loc = points[len(points) - 1]
	self.junctions.append(k)
	
    def split(self, loc):
	index = -1
	for l in range(0, len(self.path)):
		if shash(self.path[l]) == shash(loc):
			index = l
			break
	if index == -1:
		print("Error: Bad location for split")
		return
	else:
		newRoad = Road(self.name, self.path[index:])
		self.path = self.path[:index + 1]
		newRoad.numLanes = self.numLanes
		newRoad.classification = self.classification
		newRoad.speed = self.speed
		newRoad.toll = self.toll
		
		for j in range(0, len(self.junctions)):
		    inpath = 0
		    for l in self.path:
			if shash(self.junctions[j].loc)  == shash(l):
			    inpath = 1
			    break
		    if inpath == 0:
			self.junctions.pop(j)
			break
		
		newJ = StopSign([self, newRoad], []) #This must be changed to a generic junction.
		newJ.loc = loc
		self.junctions.append(newJ)
		newRoad.replaceJunction(newJ)
		return newRoad

    def getJunction(self, point):
    	if shash(self.junctions[0].loc) == shash(point):
		return self.junctions[0]
	elif shash(self.junctions[1].loc) == shash(point):
		return self.junctions[1]
	else:
		return None
    def replaceJunction(self, newJ):
    	if shash(self.junctions[0].loc) == shash(newJ.loc):
		self.junctions[0] = newJ
	elif shash(self.junctions[1].loc) == shash(newJ.loc):
		self.junctions[1] = newJ
	else:
		print("Error: Point " + str(newJ.loc) + " not a junction.")
    def cleanPath(self):
    	#either this method, or something has to deal with terrible paths and smooth out roads.
	# 1 2 3
	# 4   5  --> direction values!
	# 6 7 8
	direction = 0;
	return 0
    def containsLocation(self, loc):
	for l in self.path:
	    if shash(l) == shash(loc):
		return 1
	return 0
	
#Road Classifications - Affect how cars use the roads.  Users can modify these under advanced settings; the road chooses one by default.
#1. generic
    #This is the profile of a standard 2-lane road usually.  It's the default profile given.
#2. highway
    #This is meant for roads primarily used for thru traffic with speed limits upwards of 45 MPH.
    #Restrictions: Speed Limit must be over 45 MPH and road must have > 2 lanes.
#3. highway-2L
    #This is meant for 2-lane highways with speed limits upwards of 45 MPH.
    #Restrictions: Speed Limit must be over 45 MPH and road must have only 2 lanes.
#4. freeway
    #The freeway profile is heavily restricted.  Even in advanced settings, users cannot choose it.  This is for fast-moving highways with no lights.
    #Restrictions: Speed Limit must be >= 55 MPH and road must not have any lights or stop signs except at its start and end point.
#5. freeway-lev2
    #Reserved only for freeways with very high speed limits.
    #Restrictions: Speed Limit must be >= 65 MPH and road
#6. residential
    #For roads used only for residential purposes.
    #Restrictions: None

#For simulation purposes, many of these junctions are simplifications of their real-world counterparts.
#All junctions eventually need to be redone to work as road splitters.
class Junction(object):
	loc = [] #Where it is on the grid
	roads = []
	saved = 0
	ID = None
	type = 0
	def __init__(self, rds):
		self.roads = rds
		self.dominantRoads = []

class StopSign(Junction): #This needs to be redone, allowing for 3-way intersections. <-- isn't it redone?
	#This type of junction cycles each turn, allowing a single car from a direction.  If only one road has stop signs, then if both sides of the dominant road are clear, a car can enter.
	direction = 0;
	dominantRoads = [] #These should be the actual classes.  This means that there are stop signs on the other roads.  If no road is dominant, there are stop signs everywhere.
	def __init__(self, rds, dominants):
		super(StopSign, self).__init__(rds)
		self.dominantRoads = dominants
		self.type = 1
	def step(self):
		assert self.direction in range(0, len(self.roads))
		
		if self.direction in range(0, len(self.roads) - 1):
			self.direction += 1
		else:
			self.direction = 0

class TrafficLight(Junction):
	dominantRoads = [] #These should be the actual classes.
	timer = [30, 30] #This is calculated automatically?
	#roads[0] is opposite roads[1], and roads[2] is opposite roads[3]
	def __init__(self, rds, dominants):
		super(TrafficLight, self).__init__(rds)
		self.dominantRoads = dominants
		self.type = 2
class Roundabout(Junction): #This adds a whole new world of complication.
	#if a car is in a roundabout, then nothing else can enter for three steps.
	stepsRemaining = 3; #changed by a car when it enters a roundabout.
	def __init__(self, roads):
		super(Roundabout, self).__init__(roads)
		self.type = 3
class NullJunction(Junction):
	def __init__(self, road):
		super(NullJunction, self).__init__([road])
		self.type = 6
#1 - Stop Sign
#2 - Traffic Light
#3 - Roundabout
#4 - Ramp
#5 - Road Change
#6 - Null (Dead End)
#7? - Interchange

