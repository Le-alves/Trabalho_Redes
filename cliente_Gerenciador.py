class Cliente_Gerenciador:
    BUFFER_SIZE = 1024

    def __init__(self, socket):
        self.socket = socket
    
    def enviar_perguntas(self):
        try:
            while True:
                texto = input("Digite o texto a ser enviado ao servidor:\n")
                self.socket.send(texto.encode('utf-8'))  # Envia a pergunta ao servidor

                # Recebe a resposta do servidor
                data = self.socket.recv(self.BUFFER_SIZE)
                if not data:
                    print("Conexão encerrada pelo servidor.")
                    break

                texto_recebido = data.decode('utf-8')  # Converte os bytes em string
                print('Recebido do servidor:', texto_recebido)

                # Verifica se a conexão deve ser encerrada
                if texto_recebido.lower() == 'encerrando conexão...':
                    print('Encerrando o socket cliente!')
                    break
                
                # Pergunta sobre a origem da resposta
                origem = input("Você acha que essa resposta veio de um humano ou de uma máquina? (Humano = 1 | Máquina = 2): ")
                self.socket.send(origem.encode('utf-8'))  # Envia a resposta ao servidor

                # Recebe a mensagem de acerto ou erro do servidor
                feedback = self.socket.recv(self.BUFFER_SIZE)
                if not feedback:
                    print("Conexão encerrada pelo servidor.")
                    break

                mensagem_feedback = feedback.decode('utf-8')
                print('Feedback do servidor:', mensagem_feedback)
        except Exception as e:
            print(f"Erro na comunicação com o servidor: {e}")
        
        # Fecha o socket ao final da comunicação
        self.socket.close()
        print("Conexão encerrada.")
