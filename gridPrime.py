class grid:
	nodes = []
	roads = []
	WIDTH = 10
	HEIGHT = 10

	def __init__(w, h, self):
		self.WIDTH = w
		self.HEIGHT = h

		#makes nodes into a matrix
		for k in range(0, WIDTH):
			nodes.append([])

