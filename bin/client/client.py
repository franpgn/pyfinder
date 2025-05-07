import socket
import json
import os
import logging
import ssl

from threading import Thread
from framing import send_json, recv_json
from request_data import RequestData
from response_data import ResponseData
from user import User
from PyQt5 import QtCore

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class Client(QtCore.QObject):
    response_received = QtCore.pyqtSignal()
    def __init__(self, server_ip, server_port):
        super().__init__()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('__init__')
        self.server_ip = server_ip
        self.server_port = server_port

        self.tls_ctx = ssl.create_default_context(
            ssl.Purpose.SERVER_AUTH,
            cafile="./ca.crt"
        )
        self.tls_ctx.check_hostname = True
        self.tls_ctx.verify_mode = ssl.CERT_REQUIRED
        self.tls_ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        self.sock = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            self.logger.debug(f"Connection failed: {e}")
            raise ConnectionError(f"Could not connect to {self.server_ip}:{self.server_port}.\nError: {e}")

        self.request_id = 0
        self.receiver_thread = None
        self.lista_id = []

    def connect(self):
        try:
            if self.sock:
                try:
                    self.sock.getpeername()
                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                except OSError:
                    pass

            raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.tls_ctx.wrap_socket(
                raw,
                server_hostname=self.server_ip
            )
            self.sock.connect((self.server_ip, self.server_port))
            self.logger.debug(f"TLS handshake OK → {self.sock.version()}")
        except Exception as e:
            self.logger.debug(f"Connection failed: {e}")
            raise ConnectionError(
                f"Could not connect to {self.server_ip}:{self.server_port}.\nError: {e}"
            )

    def send_user(self, name, cpf, gender, date):
        if self.sock is None:
            self.logger.debug("Socket is None, cannot send.")
            return
        try:
            self.id_request_increment()
            user = User(name, cpf, gender, date)
            send_json(self.sock, RequestData(self.request_id, user).to_dict())
            self.logger.debug(f"Sent request {self.request_id}")
        except (BrokenPipeError, OSError) as e:
            self.logger.debug(f"[!] Failed to send data: {e}")

    def receive_response(self):
        try:
            while True:
                resp = recv_json(self.sock)
                if resp is None:
                    break
                self.save_response(
                    ResponseData.from_dict(resp)
                )
        except Exception as e:
            self.logger.debug(f"Error receiving data: {e}")

    def save_response(self, data):
        request_id = data.get_response_id()

        self.lista_id.append(request_id)

        filename = "responses.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                responses = json.load(file)
        else:
            responses = {"responses": []}

        responses["responses"].append(data.to_dict())

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(responses, file, indent=4, ensure_ascii=False)

        self.response_received.emit()
        self.logger.debug("Response saved successfully.")

    def start_receiving(self):
        self.receiver_thread = Thread(target=self.receive_response, daemon=True)
        self.receiver_thread.start()
        self.logger.debug("Receiver thread started.")

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip

    def set_server_port(self, server_port):
        self.server_port = server_port

    def id_request_increment(self):
        self.request_id += 1

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