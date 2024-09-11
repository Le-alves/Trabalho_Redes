import socket
from controle.historico  import Historico
from controle.ranking import Ranking
from controle.ia_Resposta import IA_Resposta


class Server_Gerenciador:
    
    BUFFER_SIZE = 1024

    def __init__(self, clientsocket, addr, log_callback, escolha_callback=None, resposta_callback=None):
        self.clientsocket = clientsocket
        self.addr = addr
        self.log_callback = log_callback
        self.escolha_callback = escolha_callback  # Callback para escolha (IA ou Humano)
        self.resposta_callback = resposta_callback  # Callback para resposta do Humano
        self.palpite_correto = None
        self.historico = Historico()
        self.ranking = Ranking()
        self.nome_usuario = None
        self.respostas_ia = 0
        self.respostas_humano = 0
        self.acertos_usuario = 0
        self.ia_resposta = IA_Resposta() 

    def registrar_usuario (self):
        nome = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')
        self.nome_usuario = nome
        self.log_callback(f"Usuário {nome} registrado com sucesso!")
        self.clientsocket.send(f"Bem-vindo, {nome}! Você foi registrado com sucesso.".encode('utf-8'))
       
    def gerenciar_comunicacao(self):
        self.registrar_usuario()
        try:
            while True:
                data = self.clientsocket.recv(self.BUFFER_SIZE)
                if not data:
                    self.log_callback('Conexão encerrada pelo cliente {}.'.format(self.addr))
                    break

                # Recebimento da mensagem do cliente    
                texto_recebido = data.decode('utf-8')
                self.log_callback('Recebido do cliente {} na porta {}: {}'.format(self.addr[0], self.addr[1], texto_recebido))

                #Verifica se é uma solicitação de ranking
                if texto_recebido.lower() == "ranking":
                    self.enviar_ranking()
                    continue

                # Se a mensagem for "bye", encerrará a conexão
                if texto_recebido.lower() == 'bye':
                    self.log_callback('Vai encerrar o socket do cliente {} !'.format(self.addr[0]))
                    self.clientsocket.send("Encerrando conexão...".encode('utf-8'))
                    break

                # Responder a pergunta
                resposta = self.responder_pergunta(texto_recebido)

                # Envia a resposta ao cliente
                self.clientsocket.send(resposta.encode('utf-8')) 

                # Palpite sobre quem respondeu 
                self.verificar_acerto(texto_recebido, resposta)  

        except Exception as e:
            self.log_callback(f"Erro na comunicação com o cliente {self.addr}: {e}")

        self.clientsocket.close()
        self.log_callback(f"Conexão com o cliente {self.addr} encerrada.")
       
    def responder_pergunta(self, pergunta):  

            # Exibe a pergunta no log
        self.log_callback(f"Pergunta recebida: {pergunta}")
        
        # Exibe a mensagem de escolha para o operador no log (em vez de usar input)
        self.log_callback("Quem deve responder essa pergunta? (Humano = 1 | IA = 2)")
        
        # A escolha agora será feita pela interface gráfica
        escolha = self.escolha_callback()  # Espera a escolha ser feita pela interface

        if escolha == "Humano":
            self.palpite_correto = "1"
            self.respostas_humano += 1
            resposta = self.resposta_callback()  # Espera a resposta ser inserida pela interface
        else:
            self.palpite_correto = "2"
            self.respostas_ia += 1
            self.log_callback(f"Resposta da IA: {resposta}")  # A IA gera a resposta

        # Retorna a resposta que será enviada ao cliente
        return resposta 
    

    def verificar_acerto(self,texto_recebido, resposta):
        try:
            # Recebe o feedback do cliente
            palpite = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')
            #Determina se o cliente acertou ou não 
            acertou = (palpite == self.palpite_correto)
            if acertou:
                self.acertos_usuario +=1
            
            # Atualiza o histórico com a pergunta, resposta e se o cliente acertou ou não | Nome de usuário e IP usados como identificadores
            self.historico.adicionar_entrada(self.nome_usuario, self.addr[0], texto_recebido, resposta, acertou) 

            #atualiza o ranking
            self.ranking.atualizar_ranking(self.nome_usuario, acertou)
            
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
            self.clientsocket.send(ranking.encode('utf-8'))

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

    def enviar_resumo_sessao(self):
        resumo = (f"Resumo da Sessão:\n"
                  f"Respostas fornecidas por IA: {self.respostas_ia}\n"
                  f"Respostas fornecidas por Humanos: {self.respostas_humano}\n"
                  f"Número de acertos: {self.acertos_usuario}")
        self.clientsocket.send(resumo.encode('utf-8'))

       

