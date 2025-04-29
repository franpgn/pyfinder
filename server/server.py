import socket
import json
import time
import threading

HOST = 'localhost'
PORT = 9000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

id_counter = 0
template_counter = 0  # Para alternar entre templates

print(f"[*] Servidor escutando em {HOST}:{PORT}")

# Templates diferentes
templates = [
    { "nome": "João Silva", "cpf": "123.456.789-00", "date": "1990-01-01" },
    { "nome": "Maria Souza", "cpf": "987.654.321-00", "date": "1985-05-05" },
    { "nome": "Carlos Santos", "cpf": "111.222.333-44", "date": "2000-10-10" }
]

# Criar um lock para controlar o id_counter em ambiente multithread
id_lock = threading.Lock()

def handle_client(client_socket, address):
    global id_counter, template_counter

    print(f"[+] Connected to {address[0]}:{address[1]}")

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                print(f"[!] Client {address[0]}:{address[1]} disconnected.")
                break

            decoded_data = data.decode('utf-8')
            json_data = json.loads(decoded_data)
            print(f"[>] JSON received from {address[0]}:{address[1]}:")
            print(json.dumps(json_data, indent=4, ensure_ascii=False))

            print("[*] Processing...")
            time.sleep(2)  # Simula o tempo de processamento

            with id_lock:
                id_counter += 1
                current_id = id_counter

            # Escolher template atual
            base_user = templates[template_counter]

            # Gerar 100 usuários
            users = []
            for i in range(100):
                user = {
                    "nome": f"{base_user['nome']} {i+1}",
                    "cpf": f"{i:03}.{i:03}.{i:03}-{i%100:02}",
                    "date": base_user['date']
                }
                users.append(user)

            # Montar resposta
            response_json = {
                "id": current_id,
                "data": users
            }

            # Alternar o template para a próxima resposta
            template_counter = (template_counter + 1) % 3

            # Enviar resposta
            response = json.dumps(response_json) + '\n'  # <<< importante para cliente conseguir separar
            client_socket.sendall(response.encode('utf-8'))
            print(f"[*] Response sent to {address[0]}:{address[1]} (ID: {current_id})")

    except Exception as e:
        print(f"[!] Error with client {address[0]}:{address[1]}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connection with {address[0]}:{address[1]} closed.")

try:
    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

except KeyboardInterrupt:
    print("\n[*] Shutting down server.")
    server_socket.close()
