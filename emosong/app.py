import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print('connected:', sid)
    await sio.emit('message',{'type':'intro','sid':sid})

@sio.event
async def message(sid, data):
    print('message:', data)
    await sio.emit('messsage',{'type':'message','sid':sid,'message':data})

@sio.event
async def disconnect(sid):
    print('disconnected:', sid)
