# framing.py
import struct, json, socket

# ---------- enviar ----------
def send_json(sock: socket.socket, obj: dict):
    body = json.dumps(obj, ensure_ascii=False).encode()
    sock.sendall(struct.pack(">I", len(body)) + body)   # 4-bytes len + body

# ---------- receber ----------
def recv_json(sock: socket.socket) -> dict | None:
    hdr = _read_exact(sock, 4)          # 4-bytes de tamanho
    if not hdr:                         # conexão encerrada
        return None
    (length,) = struct.unpack(">I", hdr)
    body = _read_exact(sock, length)    # corpo exato
    return json.loads(body.decode())

def _read_exact(sock: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return b''
        buf += chunk
    return buf
