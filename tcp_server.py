# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro e Lê Alves "

import socket, sys
from threading import Thread
from historico import Historico
from gerenciadorPerguntas import GerenciadorPerguntas

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def on_new_client(clientsocket,addr,modo, historico):
    gerenciador = GerenciadorPerguntas(historico, modo)

    while True:
        try:
            # Tratar a interação com o cliente
            if not gerenciador.interacao_completa(clientsocket, addr[0]):
                print(f'Vai encerrar o socket do cliente {addr[0]}!')
                clientsocket.close()
                return
        except Exception as error:
            print("Erro na conexão com o cliente!")
            return


def main(argv):

    modo = input("Escolha o modo de operação:\n1 - Automático\n2 - Controlado\nDigite 1 ou 2: ")

    if modo not in ['1', '2']:
        print("Modo inválido! O servidor será iniciado em modo automático.")
        modo = '1'

    historico = Historico()
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(clientsocket,addr, modo, historico))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])