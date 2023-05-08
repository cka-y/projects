# args = ("bin/linux/debug/executable")
# popen = subprocess.Popen(args, stdout=subprocess.PIPE)
# popen.wait()
# output = popen.stdout.read()


import os
import time

from flask import Flask, render_template
from flask_socketio import SocketIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
socketio = SocketIO(app)


class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File modified: {event.src_path}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")

    # Create a file and set up a watcher on it
    file_name = f"connected_socket_{int(time.time())}.txt"
    with open(file_name, 'w') as f:
        f.write("This file is created on socket connect.\n")

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(file_name)), recursive=False)
    observer.start()


if __name__ == '__main__':
    socketio.run(app)
