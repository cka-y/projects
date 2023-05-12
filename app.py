import os
import subprocess

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


@app.route('/start-cpp', methods=['POST'])
def start_cpp():
    args = ["bin/linux/debug/executable", "-e", "exemplaires/10_20_0.txt", "-c", "4"]
    subprocess.Popen(args, stdout=subprocess.DEVNULL)
    return 'C++ process started'


@app.route('/cpp-update', methods=['POST'])
def cpp_test():
    print(f'{80 * "*"}')
    print('Got C++ Update')
    print(f'{80 * "*"}')
    print(request.get_json())
    return 'Hello from python'


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


@socketio.on('file_create')
def on_message(data):
    client_address = request.remote_addr
    print(f"Client connected from {client_address}")
    file_name = f"connected_socket_{client_address.replace('.', '')}.txt"
    with open(file_name, 'w') as f:
        f.write("This file is created on socket connect.\n")
        print("Created file successfully")

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=file_name, recursive=False)
    observer.start()
    socketio.emit('file_created', {'message': f'File has been created --> {file_name}'})
    print('File created and process set successfully')


if __name__ == '__main__':
    print('running...')
    socketio.run(app)
