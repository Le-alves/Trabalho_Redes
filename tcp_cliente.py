# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro e Lê Alves"

import socket, sys


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

def fazer_pergunta(s):
    
    #Enviando pergunta para o servidor
    texto = input ("Digite o texto a ser enviado ao servidor:\n")
    s.send(texto.encode())

    #resposta do servidor
    resposta = s.recv(BUFFER_SIZE).decode("utf-8")
    print ("Recebido do servidor: ", resposta)

    #Palpite do cliente
    palpite = input("Você acha que a resposta veio de um humano ou de uma IA? (Humano(1) / IA(2)): ")
    s.send(palpite.encode())
    feedback = s.recv(BUFFER_SIZE).decode('utf-8')


    print(feedback)

def ver_pontuacao():
    print("Pontuação: (implemente lógica para exibir a pontuação)")

def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Servidor executando!")
            while(True):       
                print("1. Fazer pergunta")
                print("2. Ver pontuação")
                print("3. Sair")
                opcao = input("Escolha uma opção: ")
                
                if opcao == '1':
                    fazer_pergunta(s)
                elif opcao == '2':
                    ver_pontuacao()
                elif opcao == '3':
                    print("Encerrando conexão com o servidor...")
                    s.send("bye".encode())
                    break
                else:
                    print("Opção inválida!")
    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])