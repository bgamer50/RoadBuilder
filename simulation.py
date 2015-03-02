from gridPrime import Grid
from road import Road
from node import Node
from carPrime import Car
from random import randint

class Simulation:
	grid = None

	def __init__(self, g):
		self.grid = g

	#This method performs one discrete time step in the simulation.
	def step(self):
		for c in self.cars:
			if len(c.path) > 1:
				print(c.path)
				c.path = c.path[1:] #move the car up one place
				c.location = c.path[0]
			else:
				self.cars.remove(c) #remove the car if it has reached its destination

	def calculateNearestRoad(n):
		minDistance = pow(10, 10)
		nearestRoad = None
		for k in self.grid.nodes:
			if len(k.neighbors) > 0:
				z = k.dist(n)
				if z < minDistance:
					minDistance = z
					nearestRoad = k
			return nearestRoad

	def generateDestination(x, y):
		possibleDestinations = []
		for n in self.grid.nodes:
			if n.zone == 2:
				possibleDestinations.append(calculateNearestRoad(n))

		if len(possibleDestinations) == 0:
			return None
		else:
			return possibleDestinations(0, len(possibleDestinations))

	def generateTraffic(self):
		for n in self.grid.nodes:
			if n.zone == 1:
				r = calculateNearestRoad(n)
				dR = generateDestination(r[0], r[1])
				if randInt(0, 10) >= 1:
					c = Car(self.grid, r[0], r[1], dR[0], dR[1])