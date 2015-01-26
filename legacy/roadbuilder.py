#Runs the web server, uses web.py
import web
import json
from grid import Grid
import sqlite3 as sql
from car import Car
from simulation import step
from func import shash, fakeObject, cleanZones
from road import Road, Junction, TrafficLight, StopSign, Roundabout, NullJunction
#added to fix glitches

urls = ('/', "index", "/rds", "pathinfo", "/car", "carinfo", "/junc", "junctioninfo", "/update", "update", "/nameroad", "nameroad", "/sq", "squareinfo", "/road", "roadinfo", "/changeroad", "changeroad", "/styles", "styles", "/zones", "zones", "/bg", "bg", "/changejunction", "changejunction")
database = "./data/roadNetwork.db"

myGrid = Grid(94, 46)
bogus = fakeObject

class index:
	def GET(self):
		html = open("static/index.html").read()
		return html
	def POST(self):
		web.header('Content-Type', 'application/json')
		input = str(web.input()).split("'")[1]
		pointArray = json.loads(input)
		
		myGrid.insertRoad(pointArray)
		myGrid.save(database)

class roadinfo:
	def GET(self):
		connection = sql.connect(database)
		cursor = connection.cursor()
		rows = cursor.execute("select rowid, name, lanes, toll, speed, class from roads")

		rowArray = []
		for r in rows:
			rowArray.append(r)
		
		return json.dumps(rowArray)

class pathinfo:
	def GET(self):
		#This should be a try-catch
		connection = sql.connect(database)
		#connection.row_factory = sql.Row
		cursor = connection.cursor()
		rows = cursor.execute("select * from paths")
		
		rowArray = []
		for r in rows:
			rowArray.append(r)
		
		connection.commit()
		connection.close()
		return json.dumps(rowArray)

class carinfo:
	def GET(self):
		#This should be a try-catch
		#This will be changed to currentlocation, previouslocation, nextlocation
		carArray = []
		for cr in myGrid.cars:
			if len(cr.path[1]) != 0:
				carArray.append([cr.currentLocation, cr.path[1][0]])
			else:
				carArray.append([cr.currentLocation, cr.currentLocation])
		return json.dumps(carArray)

class junctioninfo:
	def GET(self):	
		#This might be a try-catch, I'm really not sure at this point.
		junctionArray = []
		#adds the junctions once to junctionArray.
		for rd in myGrid.roads:
			    j1 = rd.junctions[0]
			    j2 = rd.junctions[1]
			    bl = 0;
			    for j in junctionArray:
				  if shash(j.loc) == shash(j1.loc):
					bl = 1;
					break;
			    if bl == 0:
				junctionArray.append(j1)
		            
		            bl = 0;
			    for j in junctionArray:
				  if shash(j.loc) == shash(j2.loc):
					 bl = 1;
					 break;
			    if bl == 0:
				junctionArray.append(j2)
		
		#Puts it all into a "new format" and sends it off.
		newFormatArray = []
		for j in junctionArray:
		    newFormatArray.append([j.loc, j.type])
		return json.dumps(newFormatArray)
		
class update:
	#by calling this page, it will realize that it is time to update car positions.
	def GET(self):
		step(myGrid)

class nameroad:
	def POST(self):
		myGrid.roads[len(myGrid.roads) - 1].name = str(web.input()).split("'")[1]
		myGrid.save(database)
		myGrid.splitNewRoad(myGrid.roads[len(myGrid.roads) - 1])
		myGrid.save(database)
		#print(myGrid.roads[len(myGrid.roads) - 1].name)
		myGrid.save(database)

class changeroad:
	def POST(self):
                text = str(web.input()).split("'")[1]
                array = json.loads(text)
		for r in myGrid.roads:
			if r.ID == int(array[0]):
				break
		r.name = str(array[1])
		r.numLanes = int(array[2])
		r.toll = int(array[3])
		r.speed = int(array[4])
		r.classification = int(array[5])
		myGrid.save(database)
                #print(array)

class changejunction:
	def POST(self):
			text = str(web.input()).split("'")[1]
			print(text)
			array = json.loads(text)
			juncID = -1 * int(array[1]) - 1;
			newType = int(array[0])
			print(str(juncID) + " " + str(newType))
			for r in myGrid.roads:
					for j in r.junctions:
							if j.ID == juncID:
									if newType == 2:
										newJunc = TrafficLight(j.roads, [])
									elif newType == 1:
										newJunc = StopSign(j.roads, [])
									elif newType == 3:
										newJunc = Roundabout(j.roads)
									newJunc.loc = j.loc
									break
			for r in myGrid.roads:
				for j in range(0, len(r.junctions)):
					if shash(r.junctions[j].loc) == shash(newJunc.loc):
							r.junctions[j] = newJunc
			myGrid.save(database)

class squareinfo:
	def GET(self):
		#print(fakeObject.list)
		square = fakeObject.list
		
		#make this check if it's a junction then return below if it is
		if myGrid.isJunction(square):
		  for r in myGrid.roads:
		    for l in r.path:
		      if shash(square) == shash(l):
		      	try:
					return -1 * (1 + r.getJunction(l).ID) #sends the negative of the junction ID + 1.
			except:
					myGrid.save(database)
					return -1 * (1 + r.getJunction(l).ID) #sends the negative of the junction ID + 1.
		else:
		  for r in myGrid.roads:
		    for l in r.path:
		      if shash(square) == shash(l):
				return r.ID
	def POST(self):
		fakeObject.list = json.loads(str(web.input()).split("'")[1])

class styles:
	def GET(self):
		return open("./static/styles.css").read()

class bg:
	def GET(self):
		return open("./static/img/bg_main.jpg").read()
class zones:
        def GET(self):
		cleanZones(myGrid)
                return json.dumps(myGrid.zones)
	def POST(self):
		text = str(web.input()).split("'")[1]
		matrix = json.loads(text)
		for r in range(0, len(matrix)):
			if len(matrix[r]) != 0:
				myGrid.zones[r] = matrix[r]
                for r in range(0, len(myGrid.zones)):
                    for c in range(0, len(myGrid.zones[r])):
                        myGrid.zones[r][c] = int(myGrid.zones[r][c])
		myGrid.save(database)

if __name__ == "__main__":
	myGrid.reconstruct(database)
	c = Car([20, 8], [4, 5], [20, 8], myGrid)
	c.path = c.search(c.currentLocation, c.destination, c.currentRoad, [], 0, 0, [])
	#print(c.path)
	
	myGrid.cars.append(c)
	#myGrid.cars.append(d)
	app = web.application(urls, globals())
	app.run()