import socketio
from ..Tasks.task import add_user_to_queue

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('Client connected', sid)
    # sio.emit('')

@sio.event
def put_in_queue(sid, data):
    print('PUT IN QUEUE EVENT HERE', sid)
    print(data)
    # task.add_user_to_queue.delay(data)
    sio.emit('PUTINQUEUE', True)

@sio.event
def disconnect(sid):
    print('Client disconnected', sid)

@sio.event
def message(sid, data):
    print('Message from client:', data)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('localhost', 8765)), app)