class GerenciadorRespostas:

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
        try:
        # Aqui você faria a chamada à API de IA, como OpenAI GPT
            return f"-------------------------Resposta gerada por IA--------------------"
        except Exception as e:
            print(f"Erro ao gerar resposta via IA: {e}")
            return "Erro ao gerar resposta via IA."
    
    def gerar_resposta(self, modo, pergunta):
        if modo == '1':
            return self.gerar_resposta_humana()
        else:
            return self.gerar_resposta_ia(pergunta)

        
    def verificar_acerto(self, clientsocket, modo):
        try:
            clientsocket.send("Você acha que a resposta veio de um humano ou de uma IA? (Humano / IA)".encode('utf-8'))
            palpite = clientsocket.recv(self.BUFFER_SIZE).decode('utf-8').strip().lower()

            # Determinar se o cliente acertou
            acertou = (palpite == "humano" and modo == '1') or (palpite == 'ia' and modo == '2')

            return acertou
        except Exception as e:
            print("Erro ao verificar o acerto", e)
            return False
            
    def interacao_completa(self, clientsocket, endereco_cliente):

        pergunta = self.receber_pergunta(clientsocket)
        if not pergunta:
            return False

        print(pergunta)
        #Obter modo de resposta que o servidor escolherá
        modo = self.obter_modo_resposta()

        #gera a resposta com base na pergunta e no modo selecionado
        resposta = self.gerar_resposta(modo, pergunta)
        clientsocket.send(resposta.encode('utf-8'))

        # Verificação se o cliente acertou após enviar a resposta
        acertou = self.verificar_acerto(clientsocket, modo)
        feedback = "Você acertou!" if acertou else "Você errou!"
        clientsocket.send(feedback.encode("utf-8"))

        # Registrar no histórico
        self.historico.adicionar_entrada(endereco_cliente, pergunta, resposta, acertou)

        return True