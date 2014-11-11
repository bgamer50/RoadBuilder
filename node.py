class Node:
	x = 0 #the x coordinate
	y = 0 #the y coordinate
	neighbors = [] #neighboring nodes
	roads = [] #roads that contain this node

	def __init__(newX, newY):
		x = newX
		y = newY