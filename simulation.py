from grid import Grid
from road import Road, Junction
from carPrime import Car
from func import shash
from random import randint
from math import sqrt
from time import clock
from func import cleanZones
from copy import deepcopy as copy

#Simulation algorithms go here.

def step(g):
	for c in g.cars:
		if len(c.path[1]) > 0 and willMove(c.currentRoad().speed):
			conflict = isConflict(c, g)
			if conflict == 0 and len(c.path[1]) > 1 and not isJunction(c.path[1][0], g):
				c.currentLocation = c.path[1][0]
				c.path[1] = c.path[1][1:]
			elif conflict == 0 and len(c.path[1]) == 1 and not isJunction(c.path[1][0], g):
				c.currentLocation = c.path[1][0]
				c.path[1] = []
				g.cars.remove(c)
			elif conflict == 0 and len(c.path[1]) > 1 and isJunction(c.path[1][0], g):
				j = getJunction(c.path[1][0], g)
				if j.type == 1:
				    noStop = 0
				    for d in j.dominantRoads:
					if d.ID == c.currentRoad().ID:
					  noStop = 1
					  break
				    if noStop or randint(0, 100) <= 25:
					c.currentLocation = c.path[1][0]
					c.path[1] = c.path[1][1:]
					if len(c.path[1]) <= 1:
					    c.path[1] = []
					    g.cars.remove(c)
				elif j.type == 2:
				    if randint(0, 100) <= 50:
					c.currentLocation = c.path[1][0]
					c.path[1] = c.path[1][1:]
					if len(c.path[1]) <= 1:
					    c.path[1] = []
					    g.cars.remove(c)
				elif j.type == 3:
					c.currenLocation = c.path[1][0]
					c.path[1] = c.path[1][1:]
				elif j.type == 6:
				    c.currentLocation = c.path[1][0]
				    c.path[1] = c.path[1][1:]
		elif len(c.path[1]) <= 1:
			g.cars.remove(c)
	#z = clock()
	#handleZoneTrafficMorning(g)
	handlePureRandomTraffic(g)
	#print("time: " + str(clock() - z))
	visitedJunctions = []
	for r in g.roads:
	    for j in r.junctions:
		visited = 0
		for v in visitedJunctions:
		    if shash(v) == shash(j):
		      visited = 1
		      break
		if visited == 0:
		    visitedJunctions.append(j)
		    if j.type == 1:
			j.step()

def isConflict(c, g):
  collision = 0
  collidingCar = None
  for ca in g.cars:
	if shash(ca.currentLocation) == shash(c.path[1][0]):
		collision = 1
		collidingCar = ca
  if collision == 1 and len(collidingCar.path[1]) < 1:
    return 0
  if collision == 1 and shash(c.currentLocation) == shash(collidingCar.path[1][0]):
    return 0
  elif collision == 0:
    return 0
  return 1

def isJunction(l, g):
	for r in g.roads:
		if shash(r.path[0]) == shash(l) or shash(r.path[len(r.path) - 1]) == shash(l):
			return 1
	return 0
      
def getJunction(l, g):
	for r in g.roads:
	    if shash(r.path[0]) == shash(l) or shash(r.path[len(r.path) - 1]) == shash(l):
		for j in r.junctions:
		    if shash(j.loc) == shash(l):
			return j
	return None

def willMove(speedLimit):
    if randint(0, 100) < speedLimit:
        return 1
    return 0

def handleZoneTrafficMorning(g):
  residentialZones = []
  workplaceZones = []
  startLoc = None
  endLoc = None
  for r in range(0, len(g.zones)):
    for c in range(0, len(g.zones[r])):
        if g.zones[r][c] != 0 and g.zones[r][c] != None:
        	if g.zones[r][c] == 1:
            	   residentialZones.append([r, c])
            	elif g.zones[r][c] == 2:
            	   workplaceZones.append([r, c])
  if len(residentialZones) != 0 and len(workplaceZones) != 0:
      index = randint(0, len(residentialZones) - 1)
      startLoc = residentialZones[index]
      index = randint(0, len(workplaceZones) - 1)
      endLoc = workplaceZones[index]

  if randint(0, 100) < 100 and startLoc != None and endLoc != None:
	bestDist = 999999
	bestLoc = None
	for r in g.roads:
	    for l in r.path:
		distance = sqrt(pow(l[0] - startLoc[0], 2) + pow(l[1] - startLoc[1], 2))
		if distance < bestDist:
		    bestDist = distance
		    bestLoc = l
	startLoc = copy(bestLoc)

	bestDist = 999999
	bestLoc = None
	for r in g.roads:
	    for l in r.path:
		distance = sqrt(pow(l[0] - endLoc[0], 2) + pow(l[1] - endLoc[1], 2))
		if distance < bestDist:
		    bestDist = distance
		    bestLoc = l
	endLoc = copy(bestLoc)

	#print(str(residentialZones) + "|||" + str(workplaceZones))
	newCar = Car(startLoc, endLoc, startLoc, g) #HOME, DEST, CURLOC, GRID
	newCar.path = newCar.search(newCar.currentLocation, newCar.destination, newCar.currentRoad(), [], 0, 0, [])
	g.cars.append(newCar)
	if newCar.path[0] < 10000000000:
		print(newCar.path)
	
def handlePureRandomTraffic(g): 
    #THIS IS ACTUALLY PERFECT RANDOM TRAFFIC!!!!!!
    if randint(0, 100) < 60:
	possibleSpaces = []
	for r in g.roads: #needs to be changed
	   for l in r.path: #needs to be changed
	     possibleSpaces.append(l)
	if len(possibleSpaces) > 0:
		startLoc = possibleSpaces[randint(0, len(possibleSpaces) - 1)]
		endLoc = possibleSpaces[randint(0, len(possibleSpaces) - 1)]
		print(possibleSpaces)
		exit()
		newCar = Car(g, startLoc[0], startLoc[1], endLoc[0], endLoc[1])
		newCar.search()
	  	g.cars.append(newCar)
