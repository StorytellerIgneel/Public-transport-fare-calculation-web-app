from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()
from RESTful_APIs.routes import routes_bp
from WebSockets.data_generator import init_data_generator_socketio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


init_data_generator_socketio(socketio)

# Register blueprint for RESTful APIs
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)