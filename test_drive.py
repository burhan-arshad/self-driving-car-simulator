import socketio
import eventlet
from flask import Flask

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print('Simulator connected:', sid)
    send_control(0.0, 0.0)

def send_control(steering_angle, throttle):
    sio.emit('steer', data={
        'steering_angle': str(steering_angle),
        'throttle': str(throttle)
    })

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)

    print('Starting server on port 4567...')

    eventlet.wsgi.server(
        eventlet.listen(('', 4567)),
        app
    )