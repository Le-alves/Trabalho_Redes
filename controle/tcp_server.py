# tcp_server.py
import socket
from threading import Thread
from tela_servidor import TelaServidor  # Importando a classe de interface gráfica

# Variáveis do servidor
HOST = '127.0.0.1'  # Endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # Tamanho do buffer para recepção dos dados

def on_new_client(clientsocket, addr, tempo_espera_ia, tela_servidor):
    try:
        # Instancia o Server_Gerenciador passando o tempo de espera e a interface gráfica
        from server_Gerenciador import Server_Gerenciador
        gerenciador = Server_Gerenciador(clientsocket, addr, tempo_espera_ia, tela_servidor)
        gerenciador.gerenciar_comunicacao()  # Delegando toda a comunicação para o gerenciador
    except Exception as error:
        tela_servidor.inserir_texto(f"Erro na conexão com o novo cliente {addr}: {error}")
        clientsocket.close()

def iniciar_servidor(tempo_espera_ia, tela_servidor):
    try:
        # Inicia o socket do servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            tela_servidor.inserir_texto(f"Servidor iniciado em {HOST}:{PORT}")

            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                tela_servidor.inserir_texto(f"Cliente conectado: {addr}")

                # Cria uma nova thread para cada cliente
                t = Thread(target=on_new_client, args=(clientsocket, addr, tempo_espera_ia, tela_servidor))
                t.start()

    except Exception as error:
        tela_servidor.inserir_texto(f"Erro ao iniciar o servidor: {error}")

if __name__ == "__main__":
    # Importa e inicia a interface gráfica
    from tela_servidor import iniciar_interface_servidor

    # Iniciar a interface gráfica do servidor
    iniciar_interface_servidor()
