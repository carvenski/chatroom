#encoding=utf8
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.resource import Resource, WebSocketApplication

client_web_sockets = {}

class Chat(WebSocketApplication):
    def on_open(self, *args, **kwargs):
        client_web_sockets[id(self)] = self
        print("** [%s] client connected **" % id(self))

    def on_close(self, *args, **kwargs):
        client_web_sockets.pop(id(self))
        print("**[%s] client closed **" % id(self))

    def on_message(self, message, *args, **kwargs):
        try:
            for i in client_web_sockets.values():
                if i == self: continue
                i.ws.send(message)
        except Exception as e:
            print(e)

    def on_broadcast(self, data):
        pass


application = Resource([
    ('^/', Chat),
])


if __name__ == '__main__':
    print("************** WebSocket server started **************\n")
    WSGIServer('0.0.0.0:80', application, handler_class=WebSocketHandler).serve_forever()

