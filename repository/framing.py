import struct, json, socket

def send_json(sock: socket.socket, obj: dict):
    body = json.dumps(obj, ensure_ascii=False).encode()
    sock.sendall(struct.pack(">I", len(body)) + body)

def recv_json(sock: socket.socket) -> dict | None:
    hdr = _read_exact(sock, 4)
    if not hdr:
        return None
    (length,) = struct.unpack(">I", hdr)
    body = _read_exact(sock, length)
    return json.loads(body.decode())

def _read_exact(sock: socket.socket, n: int) -> bytes:
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return b''
        buf += chunk
    return buf
