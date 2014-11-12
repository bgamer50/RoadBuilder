##__Begin Imports__##
import tornado.ioloop, tornado.web, tornado.websocket
from tornado.options import define, options, parse_command_line
import sqlite3 as sql
import json
from gridPrime import Grid
##__End Imports__##

##__Begin Variable Definitions__##
clients = dict()
g = Grid(94, 46)
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
			data.append([n.ID, n.x, n.y, n.zone, n.juncType, n.isOccupied()])
		self.write_message(json.dumps(data))

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

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r"/", MainHandler),
		(r"/n", NodeHandler),
		(r"/r", RoadHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static/"}),
		]
		settings = {
			"debug": True,
		}
		g.load("./data/roadNetwork.db")
		tornado.web.Application.__init__(self, handlers, **settings)
##__End Class Definitions__##

##__Begin Initialization__##
if __name__ == "__main__":
	application = Application()
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
##__End Initialization__##