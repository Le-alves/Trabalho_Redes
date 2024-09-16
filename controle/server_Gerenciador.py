import socket
import time
from historico  import Historico
from ranking import Ranking
from ia_Resposta import IA_Resposta
import threading


class Server_Gerenciador:
    
    BUFFER_SIZE = 1024

    def __init__(self, clientsocket, addr, tempo_espera_ia = 2, tela_servidor=None):
        self.clientsocket = clientsocket
        self.addr = addr
        self.palpite_correto = None  # Inicializa como None
        self.historico = Historico()
        self.ranking = Ranking()
        self.nome_usuario = None
        self.respostas_ia = 0
        self.respostas_humano = 0
        self.acertos_usuario = 0
        self.ia_resposta = IA_Resposta()
        self.tempo_espera_ia = tempo_espera_ia
        self.tela_servidor = tela_servidor  # Referência à interface gráfica

    def log(self, mensagem):
        """Método para exibir logs apenas na interface gráfica."""
        if self.tela_servidor:
            self.tela_servidor.inserir_texto(mensagem)

    def registrar_usuario (self):
        nome = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')
        self.nome_usuario = nome
        self.log(f"Usuário {nome} registrado com sucesso!")
        self.clientsocket.send(f"Bem-vindo, {nome}! Você foi registrado com sucesso.".encode('utf-8'))
       
    def gerenciar_comunicacao(self):
        self.registrar_usuario()
        try:
            while True:
                data = self.clientsocket.recv(self.BUFFER_SIZE)
                if not data:
                    self.log('Conexão encerrada pelo cliente {}.'.format(self.addr))
                    break

                # Recebimento da mensagem do cliente    
                texto_recebido = data.decode('utf-8')
                self.log('Recebido do cliente {} na porta {}: {}'.format(self.addr[0], self.addr[1], texto_recebido))

                # Verifica se é uma solicitação de ranking
                if texto_recebido.lower() == "ranking":
                    self.enviar_ranking()
                    continue

                # Se a mensagem for "bye", encerrará a conexão
                if texto_recebido.lower() == 'bye':
                    self.log('Vai encerrar o socket do cliente {} !'.format(self.addr[0]))
                    self.clientsocket.send("Encerrando conexão...".encode('utf-8'))
                    break

                # Verifica se o texto recebido é um palpite (deve ser '1' ou '2')
                if texto_recebido in ("1", "2"):
                    # Processa o palpite
                    self.processar_palpite(texto_recebido)
                    continue

                # Se não for ranking, bye ou palpite, o servidor assume que é uma pergunta
                self.tela_servidor.exibir_pergunta(texto_recebido, self)  # Exibe a pergunta na interface gráfica

                # Aguardamos até que a resposta seja enviada pela interface gráfica
                # O método receber_resposta será chamado pela interface

        except Exception as e:
            self.log(f"Erro na comunicação com o cliente {self.addr}: {e}")

        self.clientsocket.close()
        self.log(f"Conexão com o cliente {self.addr} encerrada.")
       
    def receber_resposta(self, quem_responde, resposta):
        """Processa a resposta e envia ao cliente."""
        try:
            if quem_responde == "Humano":
                self.palpite_correto = "1"
                self.respostas_humano += 1
            else:
                self.palpite_correto = "2"
                self.respostas_ia += 1
                time.sleep(self.tempo_espera_ia)

            # Envia a resposta ao cliente
            self.clientsocket.send(resposta.encode('utf-8'))

            # Armazena a última resposta
            self.ultima_resposta = resposta

        except Exception as e:
            self.log(f"Erro ao enviar a resposta ao cliente: {e}")
        

    def processar_palpite(self, palpite):
        """Verifica se o cliente acertou o palpite sobre quem respondeu."""
        try:
            # Verifica se o palpite está correto com base em quem realmente respondeu (palpite_correto)
            acertou = (palpite == self.palpite_correto)

            if acertou:
                self.acertos_usuario += 1

            # Atualiza o histórico com a pergunta, resposta e se o cliente acertou ou não
            self.historico.adicionar_entrada(self.nome_usuario, self.addr[0], self.tela_servidor.pergunta_atual, self.ultima_resposta, acertou)

            # Atualiza o ranking
            self.ranking.atualizar_ranking(self.nome_usuario, acertou)

            # Mensagem de feedback para o cliente
            if acertou:
                mensagem = "Parabéns, você acertou!"
            else:
                mensagem = "Você errou."

            # Envia a mensagem ao cliente
            self.clientsocket.send(mensagem.encode('utf-8'))

            # Exibe a mensagem de feedback na interface do servidor
            self.log(f"Palpite do cliente: {'Correto' if acertou else 'Incorreto'} - {mensagem}")

        except Exception as e:
            self.log(f"Erro ao processar o palpite: {e}")

    def verificar_acerto(self, texto_recebido, resposta):
        """Verifica se o cliente acertou o palpite sobre quem respondeu (Humano ou IA)."""
        try:
            # Recebe o feedback do cliente sobre quem ele acha que respondeu
            palpite = self.clientsocket.recv(self.BUFFER_SIZE).decode('utf-8')

            # Verifica se o palpite está correto com base em quem realmente respondeu (palpite_correto)
            acertou = (palpite == self.palpite_correto)

            if acertou:
                self.acertos_usuario += 1
            
            # Atualiza o histórico com a pergunta, resposta e se o cliente acertou ou não
            self.historico.adicionar_entrada(self.nome_usuario, self.addr[0], texto_recebido, resposta, acertou)

            # Atualiza o ranking
            self.ranking.atualizar_ranking(self.nome_usuario, acertou)

            # Mensagem de feedback para o cliente
            if acertou:
                mensagem = "Parabéns, você acertou!"
            else:
                mensagem = "Você errou."

            # Envia a mensagem ao cliente
            self.clientsocket.send(mensagem.encode('utf-8'))

            # Exibe a mensagem de feedback na interface do servidor
            self.log(f"Palpite do cliente: {'Correto' if acertou else 'Incorreto'} - {mensagem}")

        except Exception as e:
            self.log(f"Erro ao processar o feedback: {e}")

    def enviar_ranking(self):

        try:
            # Calcula o ranking usando a classe Ranking
            ranking = self.ranking.exibir_ranking()
            self.clientsocket.send(ranking.encode('utf-8'))

            # Verifica se o ranking não é None antes de enviar
            if ranking:
                self.log(f"Enviando ranking ao cliente {self.addr}:")
                self.log(ranking)  # Para depuração, remove depois
                self.clientsocket.send(ranking.encode('utf-8'))
            else:
                self.clientsocket.send("Ranking não disponível.".encode('utf-8'))
        except Exception as e:
            self.log(f"Erro ao enviar o ranking: {e}")
            self.clientsocket.send("Erro ao calcular o ranking.".encode('utf-8'))

    def enviar_resumo_sessao(self):
        resumo = (f"Resumo da Sessão:\n"
                  f"Respostas fornecidas por IA: {self.respostas_ia}\n"
                  f"Respostas fornecidas por Humanos: {self.respostas_humano}\n"
                  f"Número de acertos: {self.acertos_usuario}")
        self.clientsocket.send(resumo.encode('utf-8'))

       

