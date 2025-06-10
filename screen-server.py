import pyautogui
import cv2
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def capture_screen():
    while True:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('screen_frame', jpg_as_text)
        socketio.sleep(0.05)

@socketio.on('connect')
def on_connect():
    print("PC viewer connected.")

if __name__ == "__main__":
    socketio.start_background_task(capture_screen)
    socketio.run(app, host='0.0.0.0', port=5000)
