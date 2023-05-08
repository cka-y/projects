from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    socketio.emit('status', {'message': f'User joined room {room}'}, room=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    socketio.emit('status', {'message': f'User left room {room}'}, room=room)


@socketio.on('message')
def on_message(data):
    room = data['room']
    message = data['message']
    socketio.emit('message', {'message': message}, room=room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
