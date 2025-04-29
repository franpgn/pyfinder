import multiprocessing
import os
import socket
import logging
import time

from repository.response_data import ResponseData
HOST, PORT = "localhost", 9000
def handleConnection(s: socket.socket, i):
    print("PID ATUAL:" + str(os.getpid()))
    logger = logging.getLogger('Client')
    logger.debug('Creating socket')

    logger.debug('Connecting to server')
    s.connect((HOST, PORT))
    time.sleep(2)
    # Send the data
    data = ('{ "request_id": %s, "user_data": { "name": "DANIEL FELIPE TOMM", "cpf": "", "date": "" }}'% i).encode('utf-8')

    logger.debug('Sending data: "%s"', data)
    s.sendall(data)

    # Receive a response
    logger.debug('Waiting for response')
    chunks = []
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)

    response = b''.join(chunks).decode('utf-8')
    response = ResponseData.import_response(response)
    print('Response from server: "%s"', response.to_dict())

    logger.debug('Closing socket')
    s.close()
    logger.debug('Done')

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    plist = []
    for i in range(12):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        process = multiprocessing.Process(target=handleConnection, args=(s, i))
        plist.append(process)
        process.start()