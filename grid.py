#The grid is used to unify all the different pieces of the simulation; it holds roads and junctions.
from road import *
from func import shash, cleanZones
import json
import sqlite3 as sql
import os
class Grid:
    roads = []
    zones = []
    cars = []
    numRows = 0
    numCols = 0
    def __init__(self, rows, cols):
	self.numRows = rows
	self.numCols = cols
	for r in range(0, rows):
		self.zones.append([])
		for c in range(0, cols):
			self.zones[r].append(0)

    def addRoad(self, r): #Adds the road to the grid.
	#Add the road to the grid.
	self.roads.append(r)

    def removeRoad(self, r): #This is a force method.
	if r in self.roads:
	    self.roads.remove(r)

    def setZone(self, x, y, zoneType): #This is a force method.  Zonetypes are currently 1 (residential), 2 (workplace), 3 (commercial/shopping)
	self.zones[x][y] = zoneType

    def saveRoads(self, connection, cursor): #save to database
	cs = "','"
	try:
		cursor.execute("select * from roads")
	except:
		cursor.execute("create table roads (name text, lanes int, toll int, speed int, class int)")
		cursor.execute("select * from roads")
	rows = cursor.fetchall()
	if len(rows) == 0: #simply adds everything if the road table is blank.
		for r in self.roads:
		  cursor.execute("insert into roads values('" + r.name + cs + str(r.numLanes) + cs + str(r.toll) + cs + str(r.speed) + cs + str(r.classification) + "')")
		  r.ID = cursor.lastrowid
	else:
		for r in self.roads:
			if r.ID == None:
			  cursor.execute("insert into roads values('" + r.name + cs + str(r.numLanes) + cs + str(r.toll) + cs + str(r.speed) + cs + str(r.classification) + "')")
			  r.ID = cursor.lastrowid
			else:
				cursor.execute("update roads set name='" + r.name + "' where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set lanes=" + str(r.numLanes) + " where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set toll=" + str(r.toll) + " where rowid='" + str(r.ID) + "'")
				cursor.execute("update roads set speed=" + str(r.speed) + " where rowid = '" + str(r.ID) + "'")
				cursor.execute("update roads set class=" + str(r.classification) + " where rowid = '" + str(r.ID) + "'")
	connection.commit()
	
    def saveJunctions(self, connection, cursor):
	cs = "','"
	try:
	  cursor.execute("drop table junctions")
	except:
	  pass #DO NOTHING

	cursor.execute("create table junctions (type int, roads text, dominants text, t1 int, t2 int, x int, y int)")
	
	visitedRoadIDs = []
	#set each junction ID to None.
	for r in self.roads:
	    for j in r.junctions:
		j.ID = None
		
	#check to see if junction has been put into the grid.  if it has not then it puts it there and saves the ID.
	for r in self.roads:
	    for j in r.junctions:
		if j.ID == None:
		    #make roadIDs
		    roadIDs = []
		    try:
		      for rd in j.roads:
			roadIDs.append(rd.ID)
		    except: pass
		    #make dominants
		    dominants = []
		    try:
		      for rd in j.dominantRoads:
			dominants.append(rd.ID)
		    except: pass
		    #make timer
		    timer = [0,0]
		    try:
		      timer[0] = j.timer[0]
		      timer[1] = j.timer[1]
		    except: pass
		    #insert the junction into the database.
		    cursor.execute("insert into junctions values('"+str(j.type)+cs+json.dumps(roadIDs)+ cs + json.dumps(dominants) + cs + str(timer[0])+cs+str(timer[1])+cs+str(j.loc[0])+cs+str(j.loc[1]) + "')")
		    j.ID = cursor.lastrowid
	
    def saveZones(self, connection, cursor):
	cs = "','"
	try:
	  cursor.execute("drop table zones")
	except:
	  pass #in other words, DO NOTHING
	
	cursor.execute("create table zones (x int, y int, zonetype int)")

	for r in range(0, len(self.zones)):
		for c in range(0, len(self.zones[r])):
		  zone = self.zones[r][c]
		  if zone != None:
		    cursor.execute("insert into zones values('" + str(r) + cs + str(c) + cs + str(zone) + "')")
	connection.commit()

    def savePaths(self, connection, cursor):
	cs = "','"
	try:
	  cursor.execute("drop table paths")
	except:
	  pass #in other words, DO NOTHING
	  
	cursor.execute("create table paths (roadid int, order_ int, x int, y int)")
	for r in self.roads:
	  order = 0
	  for p in r.path:
	    cursor.execute("insert into paths values('" + str(r.ID) + cs + str(order) + cs + str(p[0]) + cs + str(p[1]) + "')")
	    order += 1
	connection.commit()

    def save(self, path):
	connection = sql.connect(path)
	connection.row_factory = sql.Row
	cursor = connection.cursor()
	self.saveRoads(connection, cursor)
	self.saveJunctions(connection, cursor)
	self.saveZones(connection, cursor)
	self.savePaths(connection, cursor)
	connection.commit()
	connection.close()

    def reconstruct(self, path):
	connection = sql.connect(path)
	cursor = connection.cursor()
	roadRows = cursor.execute("select rowid, name, lanes, toll, speed, class from roads").fetchall()
	pathRows = cursor.execute("select * from paths").fetchall()
	junctionRows = cursor.execute("select rowid, type, roads, dominants, t1, t2, x, y from junctions").fetchall()
	zoneRows = cursor.execute("select * from zones").fetchall()
	#print(roadRows)
	#reconstructing roads
	for r in roadRows:
		pathPieces = cursor.execute("select x, y from paths where roadid=" + str(r[0])).fetchall()
		#print(str(r))
		newPath = []
		for p in pathPieces:
			newPath.append( [int(p[0]), int(p[1])] )
		
		newRoad = Road(str(r[1]), newPath)
		newRoad.ID = int(r[0])
		newRoad.numlanes = int(r[2])
		newRoad.toll = int(r[3])
		newRoad.speed = int(r[4])
		newRoad.classification = int(r[5])
		self.roads.append(newRoad)
	for j in junctionRows:
		roadIDs = json.loads(str(j[2]))
		#print(j[3])
		dominants = json.loads(str(j[3]))
		jRoads = []
		for i in roadIDs:
			for rrd in self.roads:
				if int(rrd.ID) == int(i):
					jRoads.append(rrd)
					break
		assert j[1] in (1, 2, 3, 6)
		#parse the array of roads to make junctions
		if int(j[1]) == 1:
			newJunc = StopSign(jRoads, [])
		elif int(j[1]) == 2:
			newJunc = TrafficLight(jRoads, dominants)
		elif int(j[1]) == 3:
			newJunc = Roundabout(jRoads)
		elif int(j[1]) == 6:
			newJunc = NullJunction(jRoads[0])
		newJunc.loc = [int(j[6]), int(j[7])]
		newJunc._timer = [int(j[4]), int(j[5])]
		newJunc.ID = int(j[0])
		#print(newJunc)
		#add the new junctions to the roads
		for rrd in newJunc.roads:
			for k in range(0, len(rrd.junctions)):
				rrdJ = rrd.junctions[k]
				if shash(rrdJ.loc) == shash(newJunc.loc):
					rrd.junctions[k] = newJunc
					#print("asdfasfsdfsdf")
	#reconstructing zones
	for z in zoneRows:
		try:
		  self.zones[int(z[0])][int(z[1])] = int(z[2])
		except:
		  pass
	for z in range(0, len(self.zones)):
		if len(self.zones[z]) != self.numCols:
			self.zones.pop(z)
	cleanZones(self)

    def isJunction(self, loc):
	for r in self.roads:
	    for j in r.junctions:
		if shash(j.loc) == shash(loc):
		   return 1
	return 0
			
    def insertRoad(self, pointArray):
	collisionLocations = []
	collisionRoads = [] #corresponds exactly to collisionLocations, each location in collisionLocations has the same index as the road it is on.
	for locIndex in range(0, len(pointArray)):
	    loc = pointArray[locIndex]
	    for rd in self.roads:
		for l in rd.path:
		    if shash(loc) == shash(l):
			collisionLocations.append(loc)
			collisionRoads.append(rd)
	newCollisionRoads = []
	#make multiple roads that form one big road.
	for cIndex in range(0, len(collisionRoads)):
	    splitR = collisionRoads[cIndex].split(collisionLocations[cIndex])
	    newCollisionRoads.append(collisionRoads[cIndex])
	    newCollisionRoads.append(splitR)
	#THIS DOES NOT WORK IF YOU INTERSECT WITH THE SAME ROAD TWICE (OR FOR THAT MATTER THE NEW ROAD ITSELF)
	
	#Make New Roads
	newRoad = Road("", pointArray)
	self.roads += newCollisionRoads + [newRoad] #The new road must be appended last.
	#THIS IS NOT DONE; A CALL MUST BE MADE TO SPLITNEWROAD

    def splitNewRoad(self, r):
	if len(r.path) == 0:
	    return
	else:
	    newR = None
	    stop = 0
	    for rd in self.roads:
		if stop == 1:
		    break
		for j in rd.junctions:
		    if r.containsLocation(j.loc) and r.getJunction(j.loc) == None:
			newR = r.split(j.loc)
			newR.replaceJunction(j)
			self.roads.append(newR)
			r.replaceJunction(j)
			j.roads.append(r)
			j.roads.append(newR)
			stop = 1
			break
	    if newR != None:
		self.splitNewRoad(newR)