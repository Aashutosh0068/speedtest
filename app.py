from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock
import serial
import time

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votes'
socketio = SocketIO(app, cors_allowed_origins='*')
ser = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=9600)


def background_thread():
    while True:
        try :
          dummy_sensor_value = ser.readline().decode('UTF-8').strip()
          print(dummy_sensor_value)
          socketio.emit('updateSensorData', {'value': dummy_sensor_value})
        except serial.SerialTimeoutException:
            pass
        time.sleep(0.05)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app)
