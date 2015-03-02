import sqlite3 as sql
import json
from road import Road
from node import Node
class Grid:
	nodes = []
	roads = []
	cars = []
	WIDTH = 10
	HEIGHT = 10

	def __init__(self, w, h):
		self.WIDTH = w
		self.HEIGHT = h
		self.nodes = []
		self.roads = []
		self.cars = []

	def saveRoads(self, filename):
		#initialize database
		connection = sql.connect(filename)
		cursor = connection.cursor()

		#check to see if table exists
		try:
			cursor.execute("select * from roads")
		#create the table if it does not exist
		except:
			cursor.execute("create table roads(name text, lanes int, toll int, speed int, class int)")
		
		#loops over each road, if not already in the table it adds it and gives it an ID.  Otherwise it just updates it.
		for r in self.roads:
			if r.ID != None:
				cursor.execute("update roads set name='" + r.name + "' where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set lanes='" + str(r.numLanes) + "' where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set toll='" + str(r.toll) + "' where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set speed='" + str(r.speed) + "' where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set class='" + str(r.classification) + "' where rowid='" + str(r.ID) + "'")
			else:
				cs = "', '"
				cursor.execute("insert into roads values('" + r.name + cs + str(r.numLanes) + cs + str(r.toll) + cs + str(r.speed) + cs + str(r.classification) + "')")
				r.ID = cursor.lastrowid
		connection.commit()

	def loadRoads(self, filename):
		#initialize database
		connection = sql.connect(filename)
		cursor = connection.cursor()

		#begin loading
		rows = cursor.execute("select name, lanes, toll, speed, class, rowid from roads")
		for rw in rows:
			r = Road(rw[0], [[]])
			r.numLanes = int(rw[1])
			r.toll = int(rw[2])
			r.speed = int(rw[3])
			r.classification = int(rw[4])
			r.ID = int(rw[5])
			self.roads.append(r)
		#there should no longer be a need to keep track of a road's path

	def saveNodes(self, filename):
		#initialize connection
		connection = sql.connect(filename)
		cursor = connection.cursor()

		#check to see if table exists
		try:
			cursor.execute("select * from nodes")
		#create table if it does not exist
		except:
			cursor.execute("create table nodes(x int, y int, zone int, neighbors text, junctype int)")

		#saves the primary field data
		for n in self.nodes:
			if n.ID == None:
				cs = "', '"
				tempArray = []
				for nb in n.neighbors:
					tempArray.append([nb[0], nb[1], nb[2].ID])
				cursor.execute("insert into nodes values('" + str(n.x) + cs + str(n.y) + cs + str(n.zone) + cs + json.dumps(tempArray) + cs + str(n.juncType) + "')")
				n.ID = cursor.lastrowid
			else:
				tempArray = []
				for nb in n.neighbors:
					tempArray.append([nb[0], nb[1], nb[2].ID])
				cursor.execute("update nodes set x='" + str(n.x) + "' where rowid='" + str(n.ID) + "'")
				cursor.execute("update nodes set y='" + str(n.y) + "' where rowid='" + str(n.ID) + "'")
				cursor.execute("update nodes set zone='" + str(n.zone) + "' where rowid='" + str(n.ID) + "'")
				cursor.execute("update nodes set neighbors='" + json.dumps(tempArray) + "' where rowid='" + str(n.ID) + "'")
				cursor.execute("update nodes set junctype='" + str(n.juncType) + "' where rowid='" + str(n.ID) + "'")
		connection.commit()

	def loadNodes(self, filename):
		#initialize connection
		connection = sql.connect(filename)
		cursor = connection.cursor()

		rows = cursor.execute("select x, y, zone, neighbors, juncType, rowid from nodes").fetchall()

		for rw in rows:
			n = Node(rw[0], rw[1])
			n.zone = rw[2]
			n.neighbors = self.recoverNeighbors(json.loads(rw[3]))
			n.juncType = rw[4]
			n.ID = rw[5]
			self.nodes.append(n)

	def recoverNeighbors(self, arr):
		neighbors = []
		for e in arr:
			for r in self.roads:
				if e[2] == r.ID:
					neighbors.append([ e[0], e[1], r ])
		return neighbors

	def save(self, filename):
		self.saveRoads(filename)
		self.saveNodes(filename)

	def load(self, filename):
		self.loadRoads(filename)
		self.loadNodes(filename)
		print(self.nodes[0].neighbors)

	def containsNode(self, x, y):
		for n in self.nodes:
			if n.x == x and n.y == y:
				return 1
		return 0

	def getNode(self, x, y):
		for n in self.nodes:
			if n.x == x and n.y == y:
				return n

	def arrayToNodes(self, array, r):
		for k in range(0, len(array)):
			e = array[k]
			if not self.containsNode(e[0], e[1]):
				n = Node(e[0], e[1])
				self.nodes.append(n)
			else:
				n = self.getNode(e[0], e[1])
			if k > 0:
				n.neighbors.append([array[k - 1][0], array[k - 1][1], r])
			if k < len(array) - 1:
				n.neighbors.append([array[k + 1][0], array[k + 1][1], r])
			if(len(n.neighbors) > 2):
				n.juncType = 1

	def getID(self, array):
		x = int(array[0])
		y = int(array[1])
		for n in self.nodes:
			if n.x == x and n.y == y:
				if n.juncType != 0:
					return -1
				elif len(n.neighbors) == 0:
					return -2
				else:
					return n.neighbors[0][2].ID
		return -2

	def updateRoad(self, array):
		for r in self.roads:
			if r.ID == int(array[0]):
				r.name = array[1]
				r.lanes = int(array[2])
				r.toll = int(array[3])
				r.speed = int(array[4])
				r.classification = int(array[5])

	def updateNode(self, array, database):
		x = int(array[0])
		y = int(array[1])
		for n in self.nodes:
			if n.x == x and n.y == y:
				if int(array[2]) == -1:
					self.nodes.remove(n)
					connection = sql.connect(database)
					connection.cursor().execute("delete from nodes where x='" + str(x) + "' and y='" + str(y) + "'")
					connection.commit()
					return
				else:
					n.zone = int(array[2])
					n.juncType = int(array[3])
					return
		
		#reaching here indicates the node needs to be created
		n = Node(x, y)
		n.zone = int(array[2])
		n.juncType = int(array[3])
		self.nodes.append(n)