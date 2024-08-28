import socket

class Server_Gerenciador:
    
    BUFFER_SIZE = 1024

    def __init__(self, clientsocket, addr):
        self.clientsocket = clientsocket
        self.addr = addr
        self.palpite_correto = None  # Inicializa o palpite_correto como None
    
    def gerenciar_comunicacao(self):
        try:
            while True:
                data = self.clientsocket.recv(self.BUFFER_SIZE)
                if not data:
                    print('Conexão encerrada pelo cliente {}.'.format(self.addr))
                    break

                # Recebimento da mensagem do cliente    
                texto_recebido = data.decode('utf-8')  # Converte os bytes em string
                print('Recebido do cliente {} na porta {}: {}'.format(self.addr[0], self.addr[1], texto_recebido))

                # Se a mensagem for "bye", encerrará a conexão
                if texto_recebido.lower() == 'bye':
                    print('Vai encerrar o socket do cliente {} !'.format(self.addr[0]))
                    self.clientsocket.send("Encerrando conexão...".encode('utf-8'))
                    break

                # Responder a pergunta
                resposta = self.responder_pergunta(texto_recebido)

                # Envia a resposta ao cliente (converte a string em bytes)
                self.clientsocket.send(resposta.encode('utf-8')) 

                # Palpite sobre quem respondeu
                self.verificar_acerto()
        except Exception as e:
            print(f"Erro na comunicação com o cliente {self.addr}: {e}")
        
        # Fecha o socket ao final da comunicação
        self.clientsocket.close()
        print(f"Conexão com o cliente {self.addr} encerrada.")
       
    def responder_pergunta(self, pergunta):  # Acrescentar a lógica da Inteligência Artificial
        if input("Quem deve responder essa pergunta? (Humano = 1 | IA = 2): ") == "1":
            self.palpite_correto = "1"
            return input("Digite a resposta para o cliente: ")
        else:
            self.palpite_correto = "2"
            return "---------------Resposta da IA---------------"

    def verificar_acerto(self):
        try:
            # Recebe o feedback do cliente
            palpite = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')
            
            # Verifica se o cliente acertou e envia a resposta de volta ao cliente
            if palpite == self.palpite_correto:
                mensagem = "Parabéns, você acertou!"
            else:
                mensagem = "Você errou"

            # Envia a mensagem de acerto ou erro ao cliente
            self.clientsocket.send(mensagem.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao processar o feedback: {e}")
