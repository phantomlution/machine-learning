from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import io
from PIL import Image
# from NeuralNetwork_1 import NeuralNetwork1
from NeuralNetwork_2 import NeuralNetwork2
from Tool import Tool
from numpy import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('image', namespace='/handwriting')
def handwriting_receive(message):
    handwriting_base64 = message['data'].split('base64,')[1]
    ori_image_data = base64.b64decode(handwriting_base64)
    buf = io.BytesIO(ori_image_data)
    original = Image.open(buf).convert('L')
    img = original.resize((28, 28))
    data = Tool.convert(img)
    numpy_data = array([data], dtype=float32) / 255
    possibility = NeuralNetwork2.compute(numpy_data)
    emit('possibility', { 'data': possibility.tolist() })


@socketio.on('connect', namespace='/handwriting')
def connect():
    print('Client connected')


@socketio.on('disconnect', namespace='/handwriting')
def disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=False)