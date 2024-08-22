class GerenciadorPerguntas:

    BUFFER_SIZE = 1024

    def __init__(self, historico, modo):
        self.historico = historico
        self.modo = modo
    
    def receber_pergunta(self, clientesocket):
        try:
            data = clientesocket.recv(self.BUFFER_SIZE)
            if data:
                return data.decode('utf-8')
            return None
        except Exception as e:
            print("Erro ao receber pergunta", e)
            return None
        
    def gerar_resposta(self):
        if self.modo == '1':
            return"Resposta gerada por IA --------------------------- (IMPLEMENTANDO)----------------------------"
        else: 
            return input("Digite a resposta que você quer enviar: ")
        
    def verificar_acerto(self, clientsocket, resposta):
        try: 
            clientsocket.send("Você acha que a resposta veio de um humano ou de uma IA? (Humano / IA)".encode('utf-8'))
            palpite = clientsocket.recv(self.BUFFER_SIZE).decode('utf-8').strip().lower()

            #Determinar se o cliente acertou
            acertou = (palpite =="humano" and self.modo == '2') or (palpite == 'ia' and self.modo == '1')

            return acertou 
        except Exception as e:
            print("Erro ao verificar o acerto", e)
            return False
        
    def interacao_completa(self, clientsocket, endereco_cliente):
        texto_recebido = self.receber_pergunta(clientsocket)
        if not texto_recebido:
            return False
        
        resposta = self.gerar_resposta()
        clientsocket.send(resposta.encode('utf-8'))

        acertou = self.verificar_acerto(clientsocket, resposta)

        #Registrar historico
        self.historico.adicionar_entrada(endereco_cliente, texto_recebido,resposta, acertou)

        # Feed back para o cliente
        feedback = "Você acertou!" if acertou else "Você errou!"
        clientsocket.send(feedback.encode("utf-8"))

        return texto_recebido != "bye"