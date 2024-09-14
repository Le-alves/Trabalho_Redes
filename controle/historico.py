import json
import os

class Historico:

    def __init__(self, filename = "historico_perguntas.json"):
        self.filename = os.path.join(os.path.dirname(__file__), "historico_perguntas.json")
        self.dados = self.carregar_dados()

    def carregar_dados(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except PermissionError:
            print(f"Erro de permissão ao tentar abrir o arquivo {self.filename}")
            return []
        except json.JSONDecodeError:
            print(f"Erro ao tentar ler o arquivo JSON {self.filename}, possivelmente corrompido.")
            return []
        
    
    def salvar_dados(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.dados, file, indent=4)
        except PermissionError:
            print(f"Erro de permissão ao tentar salvar o arquivo {self.filename}")
        except Exception as e:
            print(f"Erro desconhecido ao salvar o arquivo {self.filename}: {e}") 

    
    def adicionar_entrada(self, usuario, ip, pergunta, resposta, acertou):
        entrada = {
            "usuario": usuario,
            "ip": ip,
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

                
        # Calcula o percentual de acertos
        for  usuario, status in ranking.items():
            status["percentual de acertos"] = (status["acertos"]/ status["total"])* 100

        return ranking