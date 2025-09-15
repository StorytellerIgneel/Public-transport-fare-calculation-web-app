# client_tester.py
import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Handle connection
@sio.event
def connect():
    print("Connected to server")
    # Send starting station id (change this number as needed)
    start_station_id = 1
    print(f"Sending start station id: {start_station_id}")
    sio.emit("train_update", start_station_id)

# Handle incoming train updates
@sio.on("train_update")
def on_train_update(data):
    print(f"Received update: {data}")

# Handle disconnection
@sio.event
def disconnect():
    print("Disconnected from server")

if __name__ == "__main__":
    # Connect to your Flask-SocketIO server
    sio.connect("http://localhost:5000")
    sio.wait()
