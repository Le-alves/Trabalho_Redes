class GerenciadorPerguntas:
    def __init__(self):
        self.pontuacao = 0
        self.total_perguntas = 0

    def fazer_pergunta(self):
        return input("Digite o texto a ser enviado ao servidor:\n")
    
    def palpite_servidor(self, resposta_servidor):
        print("Recebido do servidor: ", resposta_servidor)
        palpite = input("Você acha que a resposta veio de um humano ou de uma IA? (Humano(1) / IA(2)): ")
        return palpite
    
    def registrar_potuacao(self, acertou):
        self.total_perguntas += 1
        if acertou:
            self.pontuacao +=1

    def exibir_portuacao(self):
        print(f"Pontuação: {self.pontuacao}/{self.total_perguntas} respostas corretas")