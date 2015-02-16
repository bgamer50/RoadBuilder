class Node:
	x = 0 #the x coordinate
	y = 0 #the y coordinate
	zone = 0 #the zone of the space
	ID = None #the database ID of this node
	juncType = 0 #the type of the junction if this node is a junction (1 - stop sign, 2 - traffic light, 3 - roundabout, 4 - ramp, 5 - road change, 6 - null/dead end)
	neighbors = [] #neighboring nodes (linked by roads) [x, y, road]

	def __init__(self, newX, newY):
		self.x = newX
		self.y = newY
		self.neighbors = []
		self.zone = 0
		self.ID = None

	def isOccupied(self):
		if len(self.neighbors) > 0:
			return 1
		return 0

	#returns the orientation of the node (only appliciable if it is a road.)
	def orientation(self):
		#basically orientation is either a single square (0) or 1st, 2nd, 3rd, or 4th diagonal
		if len(self.neighbors) == 0:
			return 0
		if self.neighbors[0][0] + 1 == self.x and self.neighbors[0][1] + 1 == self.y:
			return 1
		elif self.neighbors[0][0] - 1 == self.x and self.neighbors[0][1] - 1 == self.y:
			return 2
		elif self.neighbors[0][0] - 1 == self.x and self.neighbors[0][1] + 1 == self.y:
			return 3
		elif self.neighbors[0][0] + 1 == self.x and self.neighbors[0][1] - 1 == self.y:
			return 4
		else:
			return 0