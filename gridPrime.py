import sqlite3 as sql
import json
from road import Road
from node import Node
class Grid:
	nodes = []
	roads = []
	WIDTH = 10
	HEIGHT = 10

	def __init__(self, w, h):
		self.WIDTH = w
		self.HEIGHT = h
		self.nodes = []
		self.roads = []

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

		rows = cursor.execute("select x, y, zone, neighbors, rowid from nodes").fetchall()

		for rw in rows:
			n = Node(rw[0], rw[1])
			n.zone = rw[2]
			n.neighbors = self.recoverNeighbors(json.loads(rw[3]))
			n.ID = rw[4]
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