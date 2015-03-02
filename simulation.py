from grid import Grid
from road import Road
from node import Node
from car import Car
from random import randint

class Simulation:
	grid = None

	def __init__(self, g):
		self.grid = g

	#This method performs one discrete time step in the simulation.
	def step(self):
		for c in self.grid.cars:
			if len(c.path) > 1:
				print(c.path)
				c.path = c.path[1:] #move the car up one place
				c.location = c.path[0]
			else:
				self.grid.cars.remove(c) #remove the car if it has reached its destination
		self.generateTraffic()

	def calculateNearestRoad(self, n):
		minDistance = pow(10, 10)
		nearestRoad = None
		for k in self.grid.nodes:
			if len(k.neighbors) > 0:
				z = k.dist(n)
				if z < minDistance:
					minDistance = z
					nearestRoad = k
			return nearestRoad

	def generateDestination(self, x, y):
		possibleDestinations = []
		for n in self.grid.nodes:
			if n.zone == 2:
				possibleDestinations.append(self.calculateNearestRoad(n))

		if len(possibleDestinations) == 0:
			return None
		else:
			return possibleDestinations[randint(0, len(possibleDestinations) - 1)]

	def generateTraffic(self):
		for n in self.grid.nodes:
			if n.zone == 1:
				r = self.calculateNearestRoad(n)
				dR = self.generateDestination(r.x, r.y)
				if randint(0, 9) >= 1:
					c = Car(self.grid, r.x, r.y, dR.x, dR.y)
					c.search()