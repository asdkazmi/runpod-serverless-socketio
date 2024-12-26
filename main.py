import runpod
import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stop')
def stop_socketio():
    socketio.stop()
    return 'stopped'

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect(event):
    print('Client disconnected, shutting down...')
    os._exit(0)

def runpod_handler(event):
    print(event)
    socketio.run(app, host='0.0.0.0', port=3000, allow_unsafe_werkzeug=True)
    return {
        'status': 'server closed',
    }

runpod.serverless.start({
    "handler": runpod_handler
})