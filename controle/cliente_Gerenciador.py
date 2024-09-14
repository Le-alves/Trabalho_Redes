import socket
from tkinter import Tk

class Cliente_Gerenciador:
    BUFFER_SIZE = 1024

    def __init__(self, host='127.0.0.1', port=20000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def registrar_nome(self, nome):
        """
        Registra o nome do usuário no servidor.
        :param nome: Nome do usuário.
        :return: Resposta do servidor sobre o registro.
        """
        try:
            self.socket.send(nome.encode('utf-8'))  # Envia o nome ao servidor
            resposta = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')  # Recebe a resposta do servidor
            return resposta  # Retorna a confirmação de registro
        except Exception as e:
            return f"Erro ao registrar o nome: {e}"

    def menu (self):
        while True:
            print("\nMenu:")
            print("1. Fazer pergunta")
            print("2. Ver ranking")
            print("3. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.fazer_pergunta()
            elif escolha == "2":
                self.ver_ranking()
            elif escolha == "3":
                self.sair()
                break
            else:
                print("Opção inválida. Tente novamente.")
    
    def fazer_pergunta(self, pergunta):
        try:
            # Envia a pergunta ao servidor
            self.socket.send(pergunta.encode('utf-8'))

            # Verifica se o cliente deseja encerrar a conexão
            if pergunta.lower() == 'bye':
                self.sair()
                return "Encerrando a conexão com o servidor."

            # Recebe a resposta do servidor
            resposta = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
            if not resposta:
                return "Conexão encerrada pelo servidor."

            # Verifica se a conexão deve ser encerrada pelo servidor
            if resposta.lower() == 'encerrando conexão...':
                self.sair()
                return "Encerrando o socket cliente!"

            # Retorna a resposta do servidor
            return resposta

        except Exception as e:
            return f"Erro na comunicação com o servidor: {e}"

    def limpar_buffer(self):
        try:
            # Definir um timeout curto para leitura do buffer
            self.socket.settimeout(0.1)  # 0.1 segundos para tentar limpar
            while True:
                try:
                    dados = self.socket.recv(self.BUFFER_SIZE)
                    if not dados:
                        break  # Se não houver mais dados, saímos do loop
                    
                except socket.timeout:
                    break  # Sai do loop quando não há mais dados no buffer
        except Exception as e:
            print(f"Erro ao limpar o buffer: {e}")
        finally:
            # Voltando para o modo sem timeout, para não afetar futuras operações
            self.socket.settimeout(None)



    def ver_ranking(self):
        try:
            # Solicita o ranking ao servidor 
            self.socket.send("ranking".encode('utf-8'))

            # Recebe e exibe o ranking do servidor
            ranking = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')

            if not ranking:
                print("Erro ao receber o ranking ou o ranking está vazio.")
            else:
                print("\nRanking dos Usuários:\n", ranking)  # Exibe o ranking corretamente
                
            self.limpar_buffer()

        except Exception as e:
            print(f"Erro ao tentar visualizar o ranking: {e}")


    def sair (self):
        self.socket.send("bye".encode('utf-8'))
        resumo = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(resumo)
        self.socket.close()
        print("Conexão encerrada.")
        input("Pressione Enter para fechar...")
