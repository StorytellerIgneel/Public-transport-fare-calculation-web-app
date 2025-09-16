from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from .models import Train
import eventlet
import time
import random

app = Flask(__name__)
CORS (app)

socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing

#train init
train1 = Train(train_id="T1", line="KJL", current_station=1, dir=1, progress=0.0, timestamp=time.time())
train2 = Train(train_id="T2", line="KJL", current_station=37, dir=-1, progress=0.0, timestamp=time.time())
train3 = Train(train_id="T3", line="SBK", current_station=38, dir=1, progress=0.0, timestamp=time.time())
train4 = Train(train_id="T4", line="SBK", current_station=68, dir=-1, progress=0.0, timestamp=time.time())

stations = []
Trains = [train1, train2, train3, train4]

def init_data_generator_socketio(io: SocketIO):
    global socketio
    socketio = io

    # Handle client connection
    @socketio.on('connect')
    def handle_connect():
        print(f"Client {request.sid} connected") #request sid is auto assigned by socketio
        emit('message', {'msg': 'Connected to server'})

    @socketio.on('start_updates')
    def start_updates():
        socketio.start_background_task(generate_train_updates)

    def generate_train_updates():
        while True:
            for train in Trains:
                #train1 going in the forward direction
                if train.line == "KJL":
                    if (train.dir == 1 and train.current_station == 37) or (train.dir == -1 and train.current_station == 1):
                        train.dir = -(train.dir) #change direction
                elif train.line == "SBK":
                    if (train.dir == 1 and train.current_station == 68) or (train.dir == -1 and train.current_station == 38):
                        train.dir = -(train.dir) #change direction

                data = {
                    "train_id": train.train_id,
                    "line": train.line,
                    "current_station_id": train.current_station,
                    "timestamp": time.time()
                }

                socketio.emit("train_update", data)
                print(f"Train {train.train_id} at station {train.current_station} -> sent update")

                #every 2-5 seconds sleep
                train.current_station += train.dir
                eventlet.sleep(random.randint(2, 5))

    # Handle client disconnect
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client {request.sid} disconnected")
