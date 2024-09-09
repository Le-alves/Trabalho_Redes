# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket, sys
from threading import Thread
from server_Gerenciador import Server_Gerenciador


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def on_new_client(clientsocket, addr):
    try: 
        gerenciador = Server_Gerenciador(clientsocket, addr)  # Instancia o gerenciador
        gerenciador.gerenciar_comunicacao()  # Delegando toda a comunicação para o gerenciador

    except Exception as error:
        print(f"Erro na conexão com o novo cliente {addr}: {error}")
        clientsocket.close()

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(clientsocket, addr))
                t.start()
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)

if __name__ == "__main__":   
    main(sys.argv[1:])
