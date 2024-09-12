import socket


class Cliente_Gerenciador:
    BUFFER_SIZE = 1024

    def __init__(self, socket):
        self.socket = socket

    def iniciar_conexao(self):
        nome = input("Digite seu nome para registro no servidor:\n")
        self.socket.send(nome.encode('utf-8'))  # Envia o nome ao servidor
        resposta = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')
        print(resposta)  # Confirmação de registro


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
    
    def fazer_pergunta(self):
        try:
                
                texto = input("Digite o texto a ser enviado ao servidor:\n") #VERIFICAR SE O SERVER_GERENCIADOR TEM TRATAMENTO CASO RECEBA UM "BYE"
                self.socket.send(texto.encode('utf-8'))  # Envia a pergunta ao servidor

                # Recebe a resposta do servidor
                resposta = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')# Converte os bytes em string
                if not resposta:
                    print("Conexão encerrada pelo servidor.")
                    return
                print('Resposta do servidor:', resposta)


                # Verifica se a conexão deve ser encerrada
                if resposta.lower() == 'encerrando conexão...':
                    print('Encerrando o socket cliente!')
                    self.sair()
                    return
                
                # Pergunta sobre a origem da resposta
                origem = input("Você acha que essa resposta veio de um humano ou de uma máquina? (Humano = 1 | Máquina = 2): ")
                self.socket.send(origem.encode('utf-8'))  # Envia a resposta ao servidor

                # Recebe a mensagem de acerto ou erro do servidor
                feedback = self.socket.recv(self.BUFFER_SIZE)
                if not feedback:
                    print("Conexão encerrada pelo servidor.")
                    return

                mensagem_feedback = feedback.decode('utf-8')
                print('Feedback do servidor:', mensagem_feedback)
        except Exception as e:
            print(f"Erro na comunicação com o servidor: {e}")

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
