import json

class Historico:

    def __init__(self, filename = "historico_perguntas.json"):
        self.filename = filename
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        try: 
            with open(self.filename, "r") as file: #Tentar com '' para ver o que ocorre
                return json.load(file)
        except FileNotFoundError:
            return[]
        
    
    def salvar_dados(self):
        with open(self.filename, 'w') as file: 
            json.dump(self.dados, file, indent= 4) 

    
    def adicionar_entrada(self, usuario, pergunta, resposta, acertou):
        entrada = {
            "usuario": usuario,
            "pergunta": pergunta,
            "resposta": resposta,
            "acerto": acertou
        }

        self.dados.append(entrada)
        self.salvar_dados()

    def calcular_ranking(self):
        ranking = {}
        for entrada in self.dados:
            usuario = entrada["usuario"]
            acertou = entrada["acerto"]
        if usuario not in ranking: 
            ranking[usuario] = {"acertos: ": 0,"total: ":0 } #Acrescenta o usuário ao ranking
        ranking[usuario]["total"] +=1
        if acertou: # Esta maneira considera qualquer valor que seja considerado como verdadeiro, além do True
            ranking[usuario]["acertos"] += 1

        for  usuario, status in ranking.items():
            status["percentual de acertos"] = (status["acertos"]/ status["total"])* 100

        return ranking