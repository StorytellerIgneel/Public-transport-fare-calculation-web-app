from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import os
from db_scripts import database
import re
import time
import random

app = Flask(__name__)
CORS (app)
#app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing

stations = []

def init_data_generator_socketio(io: SocketIO):
    global socketio
    socketio = io

    # Handle client connection
    @socketio.on('connect')
    def handle_connect():
        print(f"Client {request.sid} connected") #request sid is auto assigned by socketio
        emit('message', {'msg': 'Connected to server'})

    # Handle chat messages
    @socketio.on('train_update')
    def train_update(start_station_id):
        current_index = stations.index(start_station_id)
    
        while (current_index < len(stations)):
            #current station id
            station_id = stations[current_index]

            data = {
                "current_station_id" : station_id,
                "timestamp": time.time()
            }

            socketio.emit("train_update", data)
            print(f"Train  at station {station_id} -> sent update")

            #every 2-5 seconds sleep
            time.sleep(random.randint(2,5))

            current_index += 1

    # Handle client disconnect
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client {request.sid} disconnected")
