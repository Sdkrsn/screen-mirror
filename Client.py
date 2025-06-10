import socket
import pygame
import io
from PIL import Image
import numpy as np
import struct

def start_client(server_ip='192.168.63.53', server_port=12345):
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    while True:
        try:
            # Receive the length of the incoming image
            length_data = client_socket.recv(8)
            if len(length_data) < 8:
                print("Error receiving data length.")
                break
            data_length = struct.unpack('L', length_data)[0]
            
            # Receive the image data
            image_data = b""
            while len(image_data) < data_length:
                packet = client_socket.recv(data_length - len(image_data))
                if not packet:
                    break
                image_data += packet
            
            # Convert the byte data to a PIL image and display it
            img = Image.open(io.BytesIO(image_data))
            img = np.array(img)
            img_surface = pygame.surfarray.make_surface(img)
            screen.blit(img_surface, (0, 0))
            pygame.display.update()
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    client_socket.close()

if __name__ == "__main__":
    start_client()
