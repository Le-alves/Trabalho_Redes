# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro e Lê Alves "

import socket, sys
from threading import Thread
from historico import Historico
from gerenciadorRespostas import GerenciadorRespostas

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def on_new_client(clientsocket,addr, historico):
    gerenciador = GerenciadorRespostas(historico)

    while True:
        try:
            # Coordena toda a interação com o cliente
            sucesso = gerenciador.interacao_completa(clientsocket, addr)
            if not sucesso:
                print(f'Encerrando a conexão com o cliente {addr[0]}!')
                clientsocket.close()
                return

        except Exception as error:
            print(f"Erro na conexão com o cliente {addr}: {error}")
            clientsocket.close()
            return

def main(argv):

    print("--------------Bem vindo, servidor---------------------------- ")
   
   

    historico = Historico()
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(clientsocket,addr, historico))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])