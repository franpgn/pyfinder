# server_mp.py
import multiprocessing
import socket, json, os, signal, sys
import sqlite3
from multiprocessing import set_start_method, Pool
from multiprocessing.pool import ThreadPool   # YES: part of "multiprocessing"
from contextlib import closing

HOST, PORT       = "0.0.0.0", 9000
DB_FILE          = "/path/to/basecpf.db"
N_IO_THREADS     = 200               # concurrent sockets
N_CPU_PROCESSES  = os.cpu_count() or 4




# ───────────────────────── DB side (runs inside worker process) ────────────────
def _init_db(db_path):
    global DB
    DB = sqlite3.connect(db_path, check_same_thread=False, uri=True, timeout=30)
    DB.execute("PRAGMA journal_mode=WAL")     # enables many parallel readers

def db_query(request: dict):
    """
    request  = {'tipo': 'cpf', 'valor': '123...'}
    returns  = list[tuple]
    """
    cur = DB.cursor()
    if request["tipo"] == "cpf":
        cur.execute("SELECT * FROM pessoas WHERE cpf = ?", (request["valor"],))
    else:
        cur.execute("SELECT * FROM pessoas WHERE nome LIKE ?", ('%' + request["valor"] + '%',))
    return cur.fetchall()


# ───────────────────────── I/O side (runs in thread) ──────────────────────────
def handle_client(sock: socket.socket, addr, db_pool: Pool):
    with closing(sock):
        try:
            raw = sock.recv(16_384)
            if not raw:
                return
            request = json.loads(raw.decode())
            rows    = db_pool.apply(db_query, (request,))   # synchronous; could use apply_async
            sock.sendall(json.dumps({"rows": rows}).encode())
        except Exception as exc:
            print(f"[{addr}] {exc}")


# ───────────────────────── Main / bootstrap ───────────────────────────────────
def main():
    set_start_method("spawn")   # cross-platform & safest
    db_pool  = Pool(processes=N_CPU_PROCESSES, initializer=_init_db, initargs=(DB_FILE,))
    io_pool  = ThreadPool(N_IO_THREADS)       # from multiprocessing.pool

    # graceful shutdown helpers -------------------------------------------------
    def _stop(signum, frame):
        print("\nShutting down …")
        io_pool.close(); io_pool.join()       # finish current clients
        db_pool.close(); db_pool.join()       # finish queued queries
        sys.exit(0)
    for s in (signal.SIGINT, signal.SIGTERM):
        signal.signal(s, _stop)
    # --------------------------------------------------------------------------

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Listening on {HOST}:{PORT}  "
              f"(I/O threads={N_IO_THREADS}, DB processes={N_CPU_PROCESSES})")

        while True:
            client_sock, addr = srv.accept()
            io_pool.apply_async(handle_client, (client_sock, addr, db_pool))



if __name__ == "__main__":
    main()



# SERVER IMPLEMENTATION (Threaded + Multiprocess DB)

import socketserver
import sqlite3
from multiprocessing import Pool, cpu_count

# Database query function (heavy CPU operation)
def db_query(cpf):
    conn = sqlite3.connect('basecpf.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE cpf = ?", (cpf,))
    result = cursor.fetchall()
    conn.close()
    return result

# Multiprocessing pool
pool = Pool(cpu_count())

class ThreadedTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            cpf = self.request.recv(1024).decode().strip()
            if not cpf:
                return

            # Heavy DB operation sent to multiprocessing pool
            result = pool.apply(db_query, (cpf,))

            response = str(result).encode('utf-8')
            self.request.sendall(response)

        finally:
            self.request.close()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

if __name__ == "__main__":
    HOST, PORT = "localhost", 9000

    with ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler) as server:
        print(f"Server running on {HOST}:{PORT}")
        server.serve_forever()



# CLIENT IMPLEMENTATION (Multithreaded requests)

import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, cpf, host='localhost', port=9000):
        super().__init__()
        self.cpf = cpf
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(f"{self.cpf}\n".encode('utf-8'))

            response = sock.recv(4096)
            print(f"CPF: {self.cpf}, Response: {response.decode('utf-8')}")

# Function to simulate multiple client requests
def simulate_client_requests(cpfs):
    threads = []
    for cpf in cpfs:
        thread = ClientThread(cpf)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Example usage
if __name__ == "__main__":
    # Example CPF numbers
    cpf_numbers = ['12345678900', '98765432100', '55555555555', '11111111111']

    simulate_client_requests(cpf_numbers)
