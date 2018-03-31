#encoding=utf8
import web
import time
import gevent

urls = (
    '/get_messages', 'Hello1',
    '/post_messages', 'Hello2'
)

app = web.application(urls, globals())
messages = [] # [('hi', 121335), ('hello', 121334)]

class Hello1:        
    def GET(self):
        REMOTE_ADDR = web.ctx.env['REMOTE_ADDR']
        last_time = int(web.input().last_time)
        global messages
        web.header('Access-Control-Allow-Origin', '*')
        t0 = time.time()
        while True:
            if not messages or int(messages[0][1]) <= last_time:
                gevent.sleep(1)
                if time.time() - t0 > 20:
                    #return ['****server no new message****']
                    return []
                continue
            else:
                i = 1
                while i < (len(messages)-1) and int(messages[i][1]) > last_time:
                    i += 1
                return map(lambda x: x[0], filter(lambda y: y[2] != REMOTE_ADDR, messages[:i]))[::-1] + [messages[0][1]]

class Hello2:        
    def GET(self):
        REMOTE_ADDR = web.ctx.env['REMOTE_ADDR']
        last_time = web.input().last_time; message = web.input().message
        global messages
        web.header('Access-Control-Allow-Origin', '*')
        messages.append((message, last_time, REMOTE_ADDR))
        messages.sort(key=lambda x: x[1], reverse=True)
            

WSGI_app = app.wsgifunc()

