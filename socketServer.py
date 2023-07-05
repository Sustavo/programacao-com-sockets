import threading
import socket
import os

# Define o diretório onde os arquivos estão localizados
base_dir = './arquivos'

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print('[*] Servidor escutando em http://localhost:8080')

def handle_request(client_socket):
    # Recebe a requisição HTTP do cliente
    request = client_socket.recv(1024).decode('utf-8')
    print('[*] Requisição recebida:\n', request)

    # Extrai o nome do arquivo da requisição
    filename = request.split()[1]

    # Verifica se o arquivo existe no diretório
    filepath = os.path.join(base_dir, filename[1:])
    if not os.path.isfile(filepath):
        # Se o arquivo não existe, envia uma resposta "404 Not Found"
        response = 'HTTP/1.1 404 Not Found\r\n\r\nArquivo não encontrado'
    else:
        # Se o arquivo existe, lê seu conteúdo
        with open(filepath, 'r') as file:
            file_content = file.read()

        # Cria a resposta HTTP com o cabeçalho e o conteúdo do arquivo
        response = 'HTTP/1.1 200 OK\r\n\r\n' + file_content

    # Envia a resposta ao cliente
    client_socket.sendall(response.encode('utf-8'))

    # Encerra a conexão com o cliente
    client_socket.close()

while True:
    # Aguarda por conexões de clientes
    client_socket, client_address = server_socket.accept()
    print('[*] Conexão aceita de:', client_address)

    # Cria uma nova thread para tratar a requisição do cliente
    client_thread = threading.Thread(target=handle_request, args=(client_socket,))
    client_thread.start()