from multiprocessing import Process
import socket
import json
import os
import sys
from repository.user import User

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.requisition = 0
        self.receiver_process = None

    def connect(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            print(f"Connected to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit()

    def send_user(self, name, cpf, date):
        user = User(name, cpf, date)
        self.add_requisition()
        data_bytes = user.export_user(self.requisition)
        self.sock.sendall(data_bytes)
        self.start_receiving()

    def receive_response(self):
        try:
            while True:
                data_bytes = self.sock.recv(4096)
                if data_bytes:
                    self.save_response(data_bytes)
        except Exception as e:
            print(f"Error receiving data: {e}")

    def save_response(self, data_bytes):
        data = json.loads(data_bytes.decode('utf-8'))
        request_id = data["id"]
        user_data = data["data"]

        filename = "responses.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                responses = json.load(file)
        else:
            responses = {"responses": []}

        if isinstance(user_data, list):
            for user in user_data:
                new_response = {
                    "id": request_id,
                    "data": user
                }
                responses["responses"].append(new_response)
        else:
            new_response = {
                "id": request_id,
                "data": user_data
            }
            responses["responses"].append(new_response)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(responses, file, indent=4)

        print("Response saved successfully.")

    def start_receiving(self):
        self.receiver_process = Process(target=self.receive_response)
        self.receiver_process.start()
        print("Receiver process started.")

    def stop_receiving(self):
        if self.receiver_process:
            self.receiver_process.terminate()
            self.receiver_process.join()
            print("Receiver process stopped.")

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def set_server_port(self, server_port):
        self.server_port = server_port

    def add_requisition(self):
        self.requisition += 1

    def close(self):
        self.stop_receiving()
        self.sock.close()

