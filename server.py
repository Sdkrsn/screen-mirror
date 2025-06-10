import socket
import pyautogui
import numpy as np
from PIL import Image
import io
import struct
import time

def capture_screen():
    # Capture the screen using pyautogui
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    # Convert to RGB and return as byte array
    pil_image = Image.fromarray(img)
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='JPEG')
    return byte_arr.getvalue()

def start_server(host='0.0.0.0', port=12345):
    # Set up server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established.")
    
    while True:
        try:
            screen_data = capture_screen()
            # Send screen data with length information
            conn.sendall(struct.pack('L', len(screen_data)) + screen_data)
            time.sleep(0.05)  # to limit screen capture speed
        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()

if __name__ == "__main__":
    start_server()
