from threading import Thread
import socket
import json
import os
import sys
from repository.user import User
from PyQt5 import QtCore

class Client(QtCore.QObject):
    response_received = QtCore.pyqtSignal()
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.requisition = 0
        self.receiver_thread = None
        self.lista_id = []

    def connect(self):
        try:
            if self.sock:
                try:
                    self.sock.getpeername()
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    print("Previous socket closed successfully before reconnecting.")
                except OSError:
                    print("Socket was not connected. Creating a new one.")

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_ip, self.server_port))
            print(f"Connected to {self.server_ip}:{self.server_port}")
        except Exception as e:
            print(f"Connection failed: {e}")
            sys.exit()

    def send_user(self, name, cpf, date):
        if self.sock is None:
            print("Socket is None, cannot send.")
            return
        try:
            user = User(name, cpf, date)
            self.add_requisition()
            data_bytes = user.export_user(self.requisition)
            self.sock.sendall(data_bytes)
            print(f"Sent request {self.requisition} successfully.")
        except (BrokenPipeError, OSError) as e:
            print(f"[!] Failed to send data: {e}")

    def receive_response(self):
        buffer = b""
        try:
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                try:
                    data = json.loads(buffer.decode('utf-8'))
                    self.save_response(json.dumps(data).encode('utf-8'))
                    buffer = b""
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"Error receiving data: {e}")

    def save_response(self, data_bytes):
        data = json.loads(data_bytes.decode('utf-8'))
        request_id = data["id"]
        user_data = data["data"]

        self.lista_id.append(request_id)

        filename = "responses.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                responses = json.load(file)
        else:
            responses = {"responses": []}

        new_response = {
            "id": request_id,
            "data": user_data  # salva diretamente, mesmo se for lista
        }
        responses["responses"].append(new_response)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(responses, file, indent=4, ensure_ascii=False)

        self.response_received.emit()
        print("Response saved successfully.")

    def start_receiving(self):
        self.receiver_thread = Thread(target=self.receive_response, daemon=True)
        self.receiver_thread.start()
        print("Receiver thread started.")

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def set_server_port(self, server_port):
        self.server_port = server_port

    def add_requisition(self):
        self.requisition += 1

    def get_lista_id(self):
        return self.lista_id

    def close(self):
        try:
            if self.sock:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                print("Socket closed successfully.")
        except Exception as e:
            print(f"Error closing socket: {e}")

        filename = "responses.json"
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"{filename} has been deleted successfully.")
            else:
                print(f"{filename} does not exist, no need to delete.")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")


