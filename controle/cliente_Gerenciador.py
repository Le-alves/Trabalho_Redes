class Cliente_Gerenciador:
    BUFFER_SIZE = 1024

    def __init__(self, socket,callback_mensagem, callback_origem ):
        self.socket = socket
        self.callback_mensagem = callback_mensagem  # A função de callback para exibir mensagens
        self.callback_origem = callback_origem

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
    
    def fazer_pergunta(self,pergunta):
        try:

                # Envia a pergunta ao servidor
                self.socket.send(pergunta.encode('utf-8'))
                
                #texto = input("Digite o texto a ser enviado ao servidor:\n") #VERIFICAR SE O SERVER_GERENCIADOR TEM TRATAMENTO CASO RECEBA UM "BYE"
                #self.socket.send(texto.encode('utf-8'))  # Envia a pergunta ao servidor

                # Recebe a resposta do servidor
                data = self.socket.recv(self.BUFFER_SIZE)
                if not data:
                    print("Conexão encerrada pelo servidor.")
                    return

                texto_recebido = data.decode('utf-8')  # Converte os bytes em string
                self.callback_mensagem(f'Recebido do servidor: {texto_recebido}')

                # Verifica se a conexão deve ser encerrada
                if texto_recebido.lower() == 'encerrando conexão...':
                    self.callback_mensagem('Encerrando o socket cliente!')
                    self.sair()
                    return
                
                # Pergunta sobre a origem da resposta - Passou para interface grafica
                origem = self.callback_origem() 
                self.socket.send(origem.encode('utf-8'))  # Envia a resposta ao servidor

                # Recebe a mensagem de acerto ou erro do servidor
                feedback = self.socket.recv(self.BUFFER_SIZE)
                if not feedback:
                    self.callback_mensagem("Conexão encerrada pelo servidor.")
                    return

                mensagem_feedback = feedback.decode('utf-8')
                self.callback_mensagem(f'Feedback do servidor: {mensagem_feedback}')
        except Exception as e:
            self.callback_mensagem(f"Erro na comunicação com o servidor: {e}")

    def ver_ranking(self):
        try:
            # Implementação para ver o ranking
            self.socket.send("ranking".encode('utf-8'))
            ranking = self.socket.recv(1024).decode('utf-8')
            self.callback_mensagem(f"Ranking: {ranking}")

        except Exception as e:
            print(f"Erro ao tentar visualizar o ranking: {e}")


    def sair (self):
        # Implementação para sair
        self.socket.send("bye".encode('utf-8'))
        resumo = self.socket.recv(1024).decode('utf-8')
        self.callback_mensagem(f"Resumo: {resumo}")
