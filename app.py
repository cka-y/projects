import itertools
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import io
import base64
import numpy
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

from generator import generate_precincts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
counter = itertools.count(start=1, step=1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-cpp/<int:identifier>', methods=['POST'])
def start_cpp(identifier):
    args = ["wsl", "bin/linux/debug/executable", "-e", "exemplaires/10_20_0.txt", "-c", "4", "-p", "-id", str(identifier)]
    subprocess.Popen(args)
    return 'C++ process started'


@app.route('/createMunicipalitiesMap', methods=['POST'])
def create_map():
    print('hello')
    identifier = next(counter)
    req_data = request.get_json()
    x = req_data['x']
    y = req_data['y']
    generate_precincts(x, y, identifier)
    return str(identifier)


@app.route('/cpp-update/<int:identifier>', methods=['POST'])
def cpp_update(identifier):
    print(f'{80 * "*"}')
    print('Got C++ Update')
    print(f'{80 * "*"}')
    group_matrix = numpy.array(request.get_json())

    with open(f'exemplaires/{identifier}.txt', 'r') as file:
        lines = file.readlines()

    # Extract the dimensions from line 1
    dimensions = lines[0].split()
    rows = int(dimensions[0])
    cols = int(dimensions[1])

    matrix = np.empty((rows, cols), dtype=int)

    # Parse the subsequent lines and populate the array
    for i in range(rows):
        row_data = lines[i + 1].split()
        for j in range(cols):
            matrix[i, j] = int(row_data[j])

    # Calculate the average for each group
    num_groups = np.max(group_matrix)
    averages = np.zeros(num_groups)

    for i in range(num_groups):
        group_sum = np.sum(matrix[group_matrix == i + 1])
        group_size = np.sum(group_matrix == i + 1)
        averages[i] = group_sum / group_size

    averages_matrix = averages[group_matrix - 1]

    cmap = colors.LinearSegmentedColormap.from_list('green_yellow', ['green', 'yellow'], 256)

    plt.imshow(averages_matrix, cmap=cmap)
    plt.axis('off')
    plt.colorbar().remove()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0, dpi=300)
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    plt.close()

    socketio.emit('value_updated', {'image': 'data:image/png;base6' + base64_image}, room=identifier)
    return 'Successfully updated user.'


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
    print('running...')
    if not os.path.exists('./exemplaires'):
        os.makedirs('exemplaires')
    socketio.run(app, port=os.environ.get("PORT", "5000"))
