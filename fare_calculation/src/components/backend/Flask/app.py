from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from RESTful_APIs.routes import routes_bp
from WebSockets.data_generator import init_data_generator_socketio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# #initialize sockets
# init_chatbot_socketio(socketio)
# # init_community_socketio(socketio)


init_data_generator_socketio(socketio)

# Register blueprint for RESTful APIs
app.register_blueprint(routes_bp)

# #register blueprint for RESTfuls
# app.register_blueprint(auth_bp, url_prefix="/auth")
# app.register_blueprint(feedback_bp, url_prefix="/feedback")
# app.register_blueprint(shelves_bp, url_prefix="/api/shelves")

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)