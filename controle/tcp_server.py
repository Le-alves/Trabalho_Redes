# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

__author__ = "Filipe Ribeiro"

import socket, sys
from threading import Thread
from controle.server_Gerenciador import Server_Gerenciador


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados
servidor_ativo = True  # Variável de controle para o loop do servidor


def on_new_client(clientsocket, addr, log_callback, escolha_callback, resposta_callback):
    try: 
        gerenciador = Server_Gerenciador(clientsocket, addr, log_callback, escolha_callback, resposta_callback)  # Instancia o gerenciador
        gerenciador.gerenciar_comunicacao()  # Delegando toda a comunicação para o gerenciador

    except Exception as error:
        log_callback(f"Erro na conexão com o novo cliente {addr}: {error}")
        clientsocket.close()
    finally:
        clientsocket.close()  # Fecha o socket do cliente ao finalizar a comunicação

def main(log_callback, escolha_callback, resposta_callback):
    global servidor_ativo
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            log_callback(f"Servidor em execução na porta {PORT}...")

            while servidor_ativo:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                # Passe os callbacks ao criar a thread
                t = Thread(target=on_new_client, args=(clientsocket, addr, log_callback, escolha_callback, resposta_callback))
                t.start()

    except Exception as error:
        log_callback("Erro na execução do servidor!")
        log_callback(str(error))
    finally:
        log_callback("Servidor encerrado.")
        server_socket.close()  # Fecha o socket quando o servidor é encerrado
if __name__ == "__main__":   
    main(sys.argv[1:])
