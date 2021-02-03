import socketio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)


@sio.event
async def connect(sid, environ):
    print('connected:', sid)
    await sio.emit('message',{'type':'me', 'data':{'sid':sid}},to=sid)

@sio.event
async def message(sid, data):
    print('message:', data)
    await sio.emit('message', {'type':'message','data':{'sid':sid, 'username':data['username'], 'message':data['message'], 'color':data['color']}}, skip_sid=sid)

@sio.event
async def disconnect(sid):
    print('disconnected:', sid)

@sio.event
async def newuser(sid, data):
    await sio.emit('message', {'type':'newuser','data':{'sid':sid, 'username':data['username']}}, skip_sid=sid)