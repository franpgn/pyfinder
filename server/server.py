import multiprocessing
import socketserver
import logging
import ssl

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
                self.process_request(request_data)
        except ConnectionResetError:
           self.logger.warning("Client dropped connection abruptly")
        finally:
            self.request.close()

    def process_request(self, request_data):
        self.server.pool.apply_async(
            Worker.database_query,
            (request_data, self.server.db_path),
            callback=lambda resp: self._send_back(resp, request_data.get_request_id()),
            error_callback=self._log_worker_error
        )

    def _send_back(self, resp, req_id):
        try:
            frame = ResponseData.import_response(resp).to_dict()
            send_json(self.request, frame)
            self.logger.debug("Sent response for request %s", req_id)
        except OSError:
            self.logger.warning("Client socket closed before we could send reply")

    def _log_worker_error(self, exc):
        self.logger.error("Worker raised: %s", exc)

    def finish(self):
        self.logger.debug('Finish')
        return super().finish()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    request_queue_size = 1000
    _tls_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    _tls_ctx.load_cert_chain(
        certfile="../tls/server.crt",
        keyfile="../tls/server.key"
    )
    _tls_ctx.minimum_version = ssl.TLSVersion.TLSv1_2

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

    def get_request(self):
        raw_sock, addr = super().get_request()
        tls_sock = self._tls_ctx.wrap_socket(raw_sock, server_side=True)
        return tls_sock, addr

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
        self.logger.debug('Pool closed.')


