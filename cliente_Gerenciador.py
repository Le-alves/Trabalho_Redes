class Cliente_Gerenciador:
    BUFFER_SIZE = 1024

    def __init__(self, socket):
        self.socket = socket


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
                data = self.socket.recv(self.BUFFER_SIZE)
                if not data:
                    print("Conexão encerrada pelo servidor.")
                    return

                texto_recebido = data.decode('utf-8')  # Converte os bytes em string
                print('Recebido do servidor:', texto_recebido)

                # Verifica se a conexão deve ser encerrada
                if texto_recebido.lower() == 'encerrando conexão...':
                    print('Encerrando o socket cliente!')
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

    def ver_ranking(self):
        try:
            # Solicita o ranking ao servidor 
            self.socket.send("ranking".encode('utf-8'))

            # Recebe o ranking do servidor de uma vez só
            ranking = self.socket.recv(self.BUFFER_SIZE).decode('utf-8')

            if not ranking:
                print("Erro ao receber o ranking ou o ranking está vazio.")
            else:
                print("\nRanking dos Usuários:\n", ranking)

        except Exception as e:
            print(f"Erro ao tentar visualizar o ranking: {e}")


    def sair (self):
        # Fecha o socket ao final da comunicação
        self.socket.close()
        print("Conexão encerrada.")
