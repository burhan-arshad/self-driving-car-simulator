import socketio
import eventlet
from flask import Flask
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from tensorflow.keras.models import load_model

sio = socketio.Server()
app = Flask(__name__)

model = load_model('self_driving_model.keras')

def preprocess_image(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255.0

    return img

def stabilize_steering(steering):
    if abs(steering) < 0.025:
        steering = 0.0

    return steering

def calculate_throttle(speed, steering):

    strength = abs(steering)

    if strength < 0.08:
        target_speed = 14.0

    elif strength < 0.15:
        target_speed = 12.5

    elif strength < 0.25:
        target_speed = 10.5

    elif strength < 0.35:
        target_speed = 8.5

    elif strength < 0.45:
        target_speed = 6.5

    else:
        target_speed = 5.0

    error = target_speed - speed

    throttle = 0.035 * error

    if speed < 3.0:
        throttle = max(
            throttle,
            0.10
        )

    if strength < 0.08 and speed < 10.0:
        throttle = max(
            throttle,
            0.12
        )

    if strength > 0.30:
        throttle = min(
            throttle,
            0.07
        )

    if strength > 0.45:
        throttle = min(
            throttle,
            0.04
        )

    if speed > target_speed + 2.0:
        throttle = 0.0

    return float(
        np.clip(
            throttle,
            0.0,
            0.18
        )
    )

@sio.on('connect')
def connect(sid, environ):

    print(
        'Simulator connected:',
        sid
    )

    send_control(
        0.0,
        0.10
    )

@sio.on('telemetry')
def telemetry(sid, data):

    speed = float(
        data['speed']
    )

    image = Image.open(
        BytesIO(
            base64.b64decode(
                data['image']
            )
        )
    )

    image = np.asarray(
        image
    )

    image = preprocess_image(
        image
    )

    image = np.expand_dims(
        image,
        axis=0
    )

    raw_steering = float(
        model.predict(
            image,
            verbose=0
        )[0][0]
    )

    steering = stabilize_steering(
        raw_steering
    )

    steering = float(
        np.clip(
            steering,
            -1.0,
            1.0
        )
    )

    throttle = calculate_throttle(
        speed,
        steering
    )

    print(
        f"Speed: {speed:.2f} | "
        f"Steering: {steering:.4f} | "
        f"Throttle: {throttle:.3f}"
    )

    send_control(
        steering,
        throttle
    )

def send_control(
    steering_angle,
    throttle
):

    sio.emit(
        'steer',
        data={
            'steering_angle': str(
                steering_angle
            ),
            'throttle': str(
                throttle
            )
        }
    )

if __name__ == '__main__':

    app = socketio.Middleware(
        sio,
        app
    )

    print(
        'Starting server on port 4567...'
    )

    eventlet.wsgi.server(
        eventlet.listen(
            ('', 4567)
        ),
        app
    )