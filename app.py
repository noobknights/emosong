import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio, static_files={
	'/':'./templates/test.html'
})


@sio.event
async def connect(sid, environ):
    print('connected: ', sid)

@sio.event
async def message(sid, data):
    print('message ', data['num'][0])
    return 'We got: '+str(data['num'][0])

@sio.event
async def disconnect(sid):
    print('disconnected: ', sid)

app = __import__(app)