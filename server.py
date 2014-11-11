##__Begin Imports__##
import tornado.ioloop, tornado.web, tornado.websocket
from tornado.options import define, options, parse_command_line
import sqlite3 as sql
import json
##__End Imports__##

##__Begin Variable Definitions__##
clients = dict()
##__End Variable Definitions__##

##__Begin Class Definitions__##
class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("./static/index.html")

class NodeHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		elf.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
    	#the message can be a request of some sort; modified node array returned
		self.write_message("node data goes here")

class RoadHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		self.id = self.get_argument("Id")
		elf.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

	def on_message(self, message):
    	#the message can be a request of some sort; modified road array returned
		self.write_message("road data goes here")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r"/", MainHandler),
		(r"/n", NodeHandler),
		(r"/r", RoadHandler),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
		]
		settings = {
			"debug": True,
		}
		tornado.web.Application.__init__(self, handlers, **settings)
##__End Class Definitions__##

##__Begin Initialization__##
if __name__ == "__main__":
	application = Application()
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
##__End Initialization__##