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
		#basically orientation is either a single square (0) or left (1) or right (2) diagonal.
		if len(self.neighbors) != 2:
			return 0
		dx1 = self.neighbors[0][0] - self.x
		dy1 = self.neighbors[0][1] - self.y
		dx2 = self.neighbors[1][0] - self.x
		dy2 = self.neighbors[1][1] - self.y

		if dx1 == dy1 and dy2 == 0:
			return 1
		elif dx2 == dy2 and dy1 == 0:
			return 1
		elif dx1 != dy1 and dy2 == 0:
			return 2
		elif dx2 != dy2 and dy1 == 0:
			return 2
		else:
			return 0