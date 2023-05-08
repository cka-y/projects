import os

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        socketio.emit('status', {'message': f'File updated {event.src_path}'})
        print(f"File modified: {event.src_path}")


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


# @socketio.on('connect')
# def on_connect():
#     client_address = request.remote_addr
#     print(f"Client connected from {client_address}")
#     file_name = f"connected_socket_{client_address.replace('.', '')}.txt"
#     with open(file_name, 'w') as f:
#         f.write("This file is created on socket connect.\n")
#
#     event_handler = FileChangeHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(file_name)), recursive=False)
#     observer.start()


if __name__ == '__main__':
    socketio.run(app)
