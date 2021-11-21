from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from engineio.payload import Payload
import json
import random
import time

Payload.max_decode_packets = 101
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

clients = {}

# 맵 크기
MAX_N = MAX_M = 30
direction_x = [1, 0, -1, 0]
direction_y = [0, 1, 0, -1]

def make_route():
    BLOCKS = []
    x, y = 1, 1
    for _ in range(random.sample(range(20, 30), 1)[0]):
        while True:
            direction = random.sample(range(0, 3), 1)[0]
            if 0 < x + direction_x[direction] <= MAX_N and 0 < y + direction_y[direction] <= MAX_M:
                x, y = x + direction_x[direction], y + direction_y[direction]
                break
        BLOCKS.append(str(x).zfill(4) + str(y).zfill(4))
    return BLOCKS


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def background_thread():
    MOVE_JSON = {
        'DATA_TYPE': 'moveCommand',
        'AGV_NO': 'temp',
        'ACTION': '1',
        'BLOCKS': []
    }
    STATE_REQUEST = {
        'DATA_TYPE': 'reportRqst',
        'AGV_NO': 'AGV'
    }
    while True:
        socketio.sleep(1)
        for AGV in clients.keys():
            MOVE_JSON['AGV_NO'] = AGV
            STATE_REQUEST['AGV_NO'] = AGV
            MOVE_JSON['BLOCKS'] = clients[AGV]['blocks']
            socketio.emit('move_request', json.dumps(MOVE_JSON), room=clients[AGV]['sid'])
            socketio.emit('state_request', json.dumps(STATE_REQUEST), room=clients[AGV]['sid'])

@socketio.on('connect')
def connect():
    global thread
    clients[request.headers['AGV_NO']] = {}
    clients[request.headers['AGV_NO']]['sid'] = request.sid
    clients[request.headers['AGV_NO']]['blocks'] = make_route()

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    print("disconnected")
    del clients[request.headers['AGV_NO']]


@socketio.on('state_report')
def state(data):
    print(str(data))
    print(time.time())
    pass

@socketio.on('alarm_report')
def alarm(data):
    print(str(data))
    pass

# test
if __name__ == "__main__":
    # socketio.run(app,host='0.0.0.0')
    socketio.run(app)
