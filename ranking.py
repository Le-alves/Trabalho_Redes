class Ranking:
    
    def __init__(self):
        self.usuarios = {}  # Dicionário para armazenar nome de usuário e suas estatísticas

    def atualizar_ranking(self, usuario, acertou):
        if usuario not in self.usuarios:
            self.usuarios[usuario] = {'acertos': 0, 'erros': 0}
        
        if acertou:
            self.usuarios[usuario]['acertos'] += 1
        else:
            self.usuarios[usuario]['erros'] += 1

    def calcular_percentual(self, usuario):
        stats = self.usuarios.get(usuario, {'acertos': 0, 'erros': 0})
        total = stats['acertos'] + stats['erros']
        if total == 0:
            return 0.0
        return (stats['acertos'] / total) * 100

    def exibir_ranking(self):
        ranking = sorted(self.usuarios.items(), key=lambda x: self.calcular_percentual(x[0]), reverse=True)
        for posicao, (usuario, stats) in enumerate(ranking, start=1):
            print(f"{posicao}. {usuario} - {self.calcular_percentual(usuario):.2f}% de acertos")