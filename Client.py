import socket
import pygame
import io
from PIL import Image
import numpy as np
import struct

def start_client(server_ip='192.168.1.114', server_port=33060):
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Screen Mirror Client")
    fullscreen = False

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Toggle fullscreen
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

        try:
            # Receive the length of the incoming image
            length_data = client_socket.recv(8)
            if len(length_data) < 4:
                print("Error receiving data length.")
                break
            data_length = struct.unpack('Q', length_data)[0]

            # Receive the image data
            image_data = b""
            while len(image_data) < data_length:
                packet = client_socket.recv(data_length - len(image_data))
                if not packet:
                    break
                image_data += packet

            # Convert the byte data to a PIL image
            img = Image.open(io.BytesIO(image_data))
            img = np.array(img)

            # Fix orientation: Rotate 90° clockwise and flip horizontally
            img = np.rot90(img, -1)
            img = np.fliplr(img)

            # Resize image to match current window size
            window_size = screen.get_size()
            img_surface = pygame.transform.smoothscale(
                pygame.surfarray.make_surface(img), window_size
            )

            screen.blit(img_surface, (0, 0))
            pygame.display.update()
            clock.tick(60)

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
