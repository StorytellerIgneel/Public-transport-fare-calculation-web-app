import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Handle connection
@sio.event
def connect():
    print("✅ Connected to server")
    # Start getting train updates
    sio.emit("start_updates")

# Handle disconnection
@sio.event
def disconnect():
    print("❌ Disconnected from server")

# Handle generic messages
@sio.on("message")
def handle_message(data):
    print("📩 Message:", data)

# Handle train updates
@sio.on("train_update")
def handle_train_update(data):
    print(f"🚆 Train Update -> {data}")

if __name__ == "__main__":
    # Adjust URL if your backend runs on another port/host
    sio.connect("http://localhost:5000")
    sio.wait()
