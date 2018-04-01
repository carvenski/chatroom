from tornado import websocket
import tornado.ioloop

clients = {}

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        if id(self) not in clients:
            clients[id(self)] = self
        print("**** [%s] client connected ****" % id(self))

    def on_message(self, message):
        for i in clients:
            if i == id(self): continue
            clients[i].write_message(message)

    def on_close(self):
        clients.pop(id(self))
        print("**** [%s] client closed ****" % id(self))

    def check_origin(self, origin):  
        return True


application = tornado.web.Application([(r"/", EchoWebSocket)])

if __name__ == "__main__":
    print("==== Websocket Server Started ====")
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()

