# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro e Lê Alves"

import socket, sys
from gerenciadorPerguntas import GerenciadorPerguntas


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 

    gerenciador = GerenciadorPerguntas()

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
                    pergunta = gerenciador.fazer_pergunta()
                    s.send(pergunta.encode())

                    resposta_servidor = s.recv(BUFFER_SIZE).decode("utf-8")
                    palpite = gerenciador.palpite_servidor(resposta_servidor)
                    s.send(palpite.encode())

                    feedback = s.recv(BUFFER_SIZE).decode("utf-8")
                    print(feedback)

                    acertou = "acertou" in feedback.lower()
                    gerenciador.registrar_potuacao(acertou)
                elif opcao == '2':
                    gerenciador.exibir_portuacao()
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