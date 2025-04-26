import socket
import json
import sys
import multiprocessing

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))

server.listen(1000)

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024)
            if not request:
                break
            print(f"Received: {request.decode('utf-8')}")
            client_socket.send(b"ACK")
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()

