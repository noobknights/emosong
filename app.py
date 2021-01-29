import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
	'/':'./templates/test.html'
})

@sio.event
async def connect(sid, environ):
    print('connected: ', sid)

@sio.event
async def my_message(sid, data):
    print('message ', data)

@sio.event
async def disconnect(sid):
    print('disconnected: ', sid)

@sio.event
async def sum(sid, data):
    result = data['num'][0] + data['num'][1]
    await sio.emit('res', {'res':result}, to=sid)