class Node:
	x = 0 #the x coordinate
	y = 0 #the y coordinate
	zone = 0 #the zone of the space
	ID = None #the database ID of this node
	neighbors = [] #neighboring nodes (linked by roads) [x, y, road]

	def __init__(self, newX, newY):
		self.x = newX
		self.y = newY

	def isJunction(self):
		if len(roads) > 1:
			return 1
		return 0