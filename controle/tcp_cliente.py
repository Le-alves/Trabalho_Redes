# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket, sys
from cliente_Gerenciador import Cliente_Gerenciador

HOST = '127.0.0.1'  # Endereço IP
PORT = 20000        # Porta utilizada pelo servidor

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Servidor conectado!")

            # Instancia o Cliente_Gerenciador e delega a interação
            cliente = Cliente_Gerenciador(s)
            cliente.iniciar_conexao() #Registro do nome do cliente
            cliente.menu()
           

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)

if __name__ == "__main__":   
    main(sys.argv[1:])
