# use python3.6
import asyncio
import websockets  

clients = {}

async def hello(websocket, path):
    print("**** [%s] client connected ****" % id(websocket))
    try:
        if id(websocket) not in clients:
            clients[id(websocket)] = websocket
        while 1:
            message = await websocket.recv()
            for i in clients:
                if i == id(websocket): continue
                await clients[i].send(message)
    except Exception:
        clients.pop(id(websocket))
        print("**** [%s] client closed ****" % id(websocket))

start_server = websockets.serve(hello, '0.0.0.0', 80)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

