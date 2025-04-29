import json
import multiprocessing
import os
import socket
import socketserver
import logging
import threading

from multiprocessing import Pool

from repository.response_data import ResponseData
from repository.worker import Worker
from repository.request_data import RequestData

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

# -*- coding: utf-8 -*-
class ServerRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('__init__')
        super().__init__(request, client_address, server)
        return

    def setup(self):
        self.logger.debug('Setup')
        return super().setup()

    def handle(self):
        self.logger.debug('Handle')
        client_ip, client_port = self.client_address
        self.logger.debug(f"Connected client IP: {client_ip}, Port: {client_port}")
        try:
            request_data = RequestData.import_request(self.request.recv(4096))
            self.logger.debug('recv()->"%s"', request_data.to_dict())
            response = pool.apply(Worker.database_query, (request_data,))
            response = ResponseData.export_response(ResponseData.import_response(response))
            self.request.sendall(response)
        finally:
            self.request.close()

    def finish(self):
        self.logger.debug('Finish')
        return super().finish()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    request_queue_size = 10
    def __init__(self, server_address, handler_class=ServerRequestHandler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Initializing...')
        super().__init__(server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('Server is Active!')
        return super().server_activate()

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug('Waiting for connections...')
        while True:
            self.handle_request()
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 9000
    pool = Pool(processes=max(1, multiprocessing.cpu_count() - 1))
    server = Server((HOST, PORT), ServerRequestHandler)
    logger = logging.getLogger('Server')
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    logger.info('Server on %s:%s', HOST, PORT)

    # Connect to the server
    # logger.debug('Creating socket')
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # logger.debug('Connecting to server')
    # s.connect((HOST, PORT))
    #
    # # Send the data
    # data = '{ "request_id": 1, "user_data": { "name": "WAGNER DA SILVA", "cpf": "", "date": "" }}'.encode('utf-8')
    #
    # message = data
    # logger.debug('Sending data: "%s"', message)
    # len_sent = s.send(message)
    #
    # # Receive a response
    # logger.debug('Waiting for response')
    # chunks = []
    # while True:
    #     chunk = s.recv(4096)
    #     if not chunk:
    #         break
    #     chunks.append(chunk)
    #
    # response = b''.join(chunks).decode('utf-8')
    # response = ResponseData.import_response(response)
    # logger.debug('Response from server: "%s"', response.to_dict())
    #
    # # Clean up
    # logger.debug('Closing socket')
    # # s.close()
    # logger.debug('Done')