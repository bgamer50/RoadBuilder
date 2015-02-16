##__Begin Imports__##
import tornado.ioloop, tornado.web, tornado.websocket
from tornado.options import define, options, parse_command_line
import sqlite3 as sql
import json
from gridPrime import Grid
from road import Road
from carPrime import Car
from simulation import step
##__End Imports__##

##__Begin Variable Definitions__##
clients = dict()
g = Grid(94, 46)
database = "./data/roadNetwork.db"
##__End Variable Definitions__##

##__Begin Class Definitions__##
class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("./static/index.html")

class NodeHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		self.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
    	#the message can be a request of some sort; modified node array returned
		data = []
		for n in g.nodes:
			data.append([n.ID, n.x, n.y, n.zone, n.juncType, n.isOccupied(), n.orientation()])
		self.write_message(json.dumps(data))
		self.close()

class RoadHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		self.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
    	#the message can be a request of some sort; modified road array returned
		data = []
		for r in g.roads:
			data.append([r.ID, r.name, r.numLanes, r.toll, r.speed, r.classification])
		self.write_message(json.dumps(data))
		self.close()

class NewRoadHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		self.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
		parsedMessage = json.loads(message)
		r = Road(parsedMessage[0], [[]])
		g.roads.append(r)
		g.arrayToNodes(parsedMessage[1], r)
		g.save(database)
		self.close()

		#must take parsedMessage[1], the path of the road, and turn it into nodes.

class SquareInfoHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		#self.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}
		
	def on_message(self, message):
		parsedMessage = json.loads(message)
		self.write_message(str(g.getID(parsedMessage)))
		self.close()

class RoadUpdateHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
		print("updateroad " + str(message))
		parsedMessage = json.loads(message)
		g.updateRoad(parsedMessage)
		g.save(database)
		self.close()

class NodeUpdateHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
		parsedMessage = json.loads(message)
		g.updateNode(parsedMessage, database)
		g.save(database)
		self.close()

class CarHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
		parsedMessage = int(message);
		if parsedMessage == 1:
			step(g)
		carMatrix = []
		for c in g.cars:
			carMatrix.append(c.location)
		self.write_message(json.dumps(carMatrix))
		self.close()

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r"/", MainHandler),
		(r"/n", NodeHandler),
		(r"/r", RoadHandler),
		(r"/s", NewRoadHandler),
		(r"/sq", SquareInfoHandler),
		(r"/ur", RoadUpdateHandler),
		(r"/un", NodeUpdateHandler),
		(r"/car", CarHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static/"}),
		]
		settings = {
			"debug": True,
		}
		g.load("./data/roadNetwork.db")
		c = Car(g, 1, 0, 4, 0)
		c.search()
		print("path" + str(c.path))
		g.cars.append(c)
		tornado.web.Application.__init__(self, handlers, **settings)
##__End Class Definitions__##

##__Begin Initialization__##
if __name__ == "__main__":
	application = Application()
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
##__End Initialization__##