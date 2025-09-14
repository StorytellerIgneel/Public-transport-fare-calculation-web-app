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

def init_community_socketio(io: SocketIO):
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
        


    #used when the user have already joined a room, and sends message into it
    @socketio.on('send_message')
    def handle_message(data):
        msg = data['msg']
        username = data['username']
        user_id = data["user_id"]
        print(user_rooms)
        room = user_rooms[request.sid]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        emit('message', 
            {'username': username, 
            'msg': msg
            },
            room=room)
        
        match = re.search(r"room-(\d+)", room)

        if match:
            room_id = match.group(1)
            print(room_id) 

        db.execute_query('INSERT INTO messages (room_id, user_id, msg, timestamp) VALUES (?, ?, ?, ?)', (room_id, user_id, msg, timestamp))
        print(f"Message: {msg}")

    # Handle client disconnect
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client {request.sid} disconnected")
