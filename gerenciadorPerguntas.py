class GerenciadorPerguntas:

    BUFFER_SIZE = 1024

    def __init__(self, historico):
        """ Inicializa o Gerenciador com o histórico das interações."""
        self.historico = historico
        
    
    def receber_pergunta(self, clientesocket):
        try:
            data = clientesocket.recv(self.BUFFER_SIZE)
            if data:
                return data.decode('utf-8')
            return None
        except Exception as e:
            print("Erro ao receber pergunta", e)
            return None
        
    def obter_modo_resposta(self):
        while True:
            modo = input("Quem deve responder? (1 - Humano | 2 - IA): ")
            if modo in ['1','2']:
                return modo
            print("Opção inválida. Tente novamente.")
        
    def gerar_resposta_humana(self):
        return input("Digite a resposta que você quer enviar: ")
    
    def gerar_resposta_ia(self, pergunta):
        return print(f"Resposta gerada automaticamente para: {pergunta} (IA)")
    
    def gerar_resposta(self, modo, pergunta):
        if modo == '1':
            return self.gerar_resposta_humana()
        else:
            return self.gerar_resposta_ia(pergunta)

        
    def verificar_acerto(self, clientsocket, resposta):
        try: 
            clientsocket.send("Você acha que a resposta veio de um humano ou de uma IA? (Humano / IA)".encode('utf-8'))
            palpite = clientsocket.recv(self.BUFFER_SIZE).decode('utf-8').strip().lower()

            #Determinar se o cliente acertou
            acertou = (palpite =="humano" and self.modo == '1') or (palpite == 'ia' and self.modo == '2')

            return acertou 
        except Exception as e:
            print("Erro ao verificar o acerto", e)
            return False
        
    def interacao_completa(self, clientsocket, endereco_cliente):

        pergunta = self.receber_pergunta(clientsocket)
        if not pergunta:
            return False

        print(pergunta)
        modo = self.obter_modo_resposta()
        resposta = self.gerar_resposta(modo, pergunta)
        clientsocket.send(resposta.encode('utf-8'))

        acertou = self.verificar_acerto(clientsocket, modo)
        feedback = "Você acertou!" if acertou else "Você errou!"
        clientsocket.send(feedback.encode("utf-8"))

        # Registrar no histórico
        self.historico.adicionar_entrada(endereco_cliente, pergunta, resposta, acertou)

        return pergunta != "bye"