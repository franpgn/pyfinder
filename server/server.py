import multiprocessing
import socketserver
import logging

from multiprocessing import Pool
from repository.framing import recv_json, send_json
from repository.response_data import ResponseData
from repository.worker import Worker
from repository.request_data import RequestData

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

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
            while True:
                request = recv_json(self.request)
                if not request:
                    break
                request_data = RequestData.from_dict(request)
                self.logger.debug('recv()->"%s"', request_data.to_dict())
                response = self.process_request(request_data)
                send_json(self.request, response)
        except ConnectionResetError:
           self.logger.warning("Client dropped connection abruptly")
        finally:
            self.request.close()

    def process_request(self, request_data):
        self.logger.debug('Processing request...')
        resp = self.server.pool.apply(
            Worker.database_query,
            (request_data, self.server.db_path)
        )
        return ResponseData.import_response(resp).to_dict()

    def finish(self):
        self.logger.debug('Finish')
        return super().finish()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    request_queue_size = 1000
    def __init__(self, server_address, handler_class=ServerRequestHandler, workers: int = None, db_path: str = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Initializing...')
        self.db_path = db_path
        super().__init__(server_address, handler_class)
        if workers is None:
            workers = max(1, multiprocessing.cpu_count() - 1)
        self.pool = Pool(processes=workers)
        self.logger.debug(f"Server pool created with {workers} workers.")
        return

    def server_activate(self):
        self.logger.debug('Server is Active!')
        return super().server_activate()

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug('Waiting for connections...')
        while True:
            self.handle_request()
        return

    def shutdown(self):
        self.logger.debug('Shutting down server and pool...')
        super().shutdown()
        self.pool.close()
        self.pool.join()
        self.logger.debug('Pool closed.')
