import socket
from historico  import Historico
from ranking import Ranking

class Server_Gerenciador:
    
    BUFFER_SIZE = 1024

    def __init__(self, clientsocket, addr):
        self.clientsocket = clientsocket
        self.addr = addr
        self.palpite_correto = None  # Inicializa como None
        self.historico = Historico()
        self.ranking = Ranking()
    
    def gerenciar_comunicacao(self):
        try:
            while True:
                data = self.clientsocket.recv(self.BUFFER_SIZE)
                if not data:
                    print('Conexão encerrada pelo cliente {}.'.format(self.addr))
                    break

                # Recebimento da mensagem do cliente    
                texto_recebido = data.decode('utf-8')
                print('Recebido do cliente {} na porta {}: {}'.format(self.addr[0], self.addr[1], texto_recebido))

                #Verifica se é uma solicitação de ranking
                if texto_recebido.lower() == "ranking":
                    self.enviar_ranking()
                    continue

                # Se a mensagem for "bye", encerrará a conexão
                if texto_recebido.lower() == 'bye':
                    print('Vai encerrar o socket do cliente {} !'.format(self.addr[0]))
                    self.clientsocket.send("Encerrando conexão...".encode('utf-8'))
                    break

                # Responder a pergunta
                resposta = self.responder_pergunta(texto_recebido)

                # Envia a resposta ao cliente
                self.clientsocket.send(resposta.encode('utf-8')) 

                # Palpite sobre quem respondeu - PASSAR ARGUMENTOS CORRETOS
                self.verificar_acerto(texto_recebido, resposta)  # Aqui você passa os argumentos corretamente
        except Exception as e:
            print(f"Erro na comunicação com o cliente {self.addr}: {e}")

        self.clientsocket.close()
        print(f"Conexão com o cliente {self.addr} encerrada.")
       
    def responder_pergunta(self, pergunta):  # Acrescentar a lógica da Inteligência Artificial
        if input("Quem deve responder essa pergunta? (Humano = 1 | IA = 2): ") == "1":
            self.palpite_correto = "1"
            return input("Digite a resposta para o cliente: ")
        else:
            self.palpite_correto = "2"
            return "---------------Resposta da IA---------------"

    def verificar_acerto(self,texto_recebido, resposta):
        try:
            # Recebe o feedback do cliente
            palpite = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')

            #Determina se o cliente acertou ou não 
            acertou = (palpite == self.palpite_correto)
            
            #Atualiza o historico com a pergunta, resposta e se o cliente acertou ou não | IP usado como identificador
            usuario = self.addr[0]
            self.historico.adicionar_entrada(usuario, texto_recebido, resposta, acertou) 

            #atualiza o ranking
            self.ranking.atualizar_ranking(usuario, acertou)
            
            # Verificação
            if acertou:
                mensagem = "Parabéns, você acertou!"
            else:
                mensagem = "Você errou"

            # Envia a mensagem ao cliente
            self.clientsocket.send(mensagem.encode('utf-8'))

        except Exception as e:
            print(f"Erro ao processar o feedback: {e}")

    def enviar_ranking(self):

        try:
            # Calcula o ranking usando a classe Ranking
            ranking = self.ranking.exibir_ranking()

            # Verifica se o ranking não é None antes de enviar
            if ranking:
                print(f"Enviando ranking ao cliente {self.addr}:")
                print(ranking)  # Para depuração, remove depois
                self.clientsocket.send(ranking.encode('utf-8'))
            else:
                self.clientsocket.send("Ranking não disponível.".encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar o ranking: {e}")
            self.clientsocket.send("Erro ao calcular o ranking.".encode('utf-8'))

       

