import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time

class TelaServidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Teste de Turing")

        # Caixa de texto para exibir os logs do servidor
        self.output_texto = scrolledtext.ScrolledText(self.root, height=15, width=70)
        self.output_texto.grid(row=0, column=0, padx=10, pady=10)

        # Área para exibir perguntas recebidas
        self.label_pergunta = tk.Label(self.root, text="Pergunta recebida:")
        self.label_pergunta.grid(row=1, column=0, padx=10, pady=10)

        self.pergunta_recebida = tk.Label(self.root, text="")
        self.pergunta_recebida.grid(row=2, column=0, padx=10, pady=10)

        # Botões para escolher quem vai responder (Humano ou IA)
        self.botao_humano = tk.Button(self.root, text="Humano", command=self.escolher_humano, state='disabled')
        self.botao_humano.grid(row=3, column=0, padx=5, pady=5)

        self.botao_ia = tk.Button(self.root, text="IA", command=self.escolher_ia, state='disabled')
        self.botao_ia.grid(row=3, column=1, padx=5, pady=5)

        # Campo para entrada manual da resposta (se Humano for escolhido)
        self.label_resposta = tk.Label(self.root, text="Digite a resposta:", state='disabled')
        self.label_resposta.grid(row=4, column=0, padx=10, pady=10)

        self.input_resposta = tk.Entry(self.root, state='disabled')
        self.input_resposta.grid(row=5, column=0, padx=10, pady=10)

        # Botão para enviar a resposta
        self.botao_enviar_resposta = tk.Button(self.root, text="Enviar Resposta", command=self.enviar_resposta, state='disabled')
        self.botao_enviar_resposta.grid(row=6, column=0, padx=10, pady=10)

        # Variáveis de controle
        self.gerenciador_atual = None
        self.quem_responde = None
        self.pergunta_atual = ""

    def exibir_pergunta(self, pergunta, gerenciador):
        """Exibe a pergunta recebida e permite escolher quem responde."""
        self.pergunta_atual = pergunta
        self.gerenciador_atual = gerenciador
        self.pergunta_recebida.config(text=pergunta)
        
        # Habilita os botões de escolha e o campo de resposta
        self.botao_humano.config(state='normal')
        self.botao_ia.config(state='normal')

    def escolher_humano(self):
        """Define que o Humano vai responder."""
        self.quem_responde = "Humano"
        self.label_resposta.config(state='normal')
        self.input_resposta.config(state='normal')
        self.botao_enviar_resposta.config(state='normal')

    def escolher_ia(self):
        """Define que a IA vai responder."""
        self.quem_responde = "IA"
        self.label_resposta.config(state='disabled')
        self.input_resposta.config(state='disabled')
        self.botao_enviar_resposta.config(state='normal')

    def enviar_resposta(self):
        """Envia a resposta ao Server_Gerenciador."""
        if self.quem_responde == "Humano":
            resposta = self.input_resposta.get()
            self.gerenciador_atual.receber_resposta("Humano", resposta)
        else:
            self.gerenciador_atual.receber_resposta("IA")
        
        # Desabilitar os botões e campos novamente após enviar a resposta
        self.botao_humano.config(state='disabled')
        self.botao_ia.config(state='disabled')
        self.botao_enviar_resposta.config(state='disabled')
        self.input_resposta.config(state='disabled')
        self.label_resposta.config(state='disabled')
        self.input_resposta.delete(0, tk.END)  # Limpar campo de resposta

    def inserir_texto(self, mensagem):
        """Método para inserir texto na interface gráfica."""
        self.output_texto.insert(tk.END, mensagem + "\n")
        self.output_texto.yview(tk.END)  # Scroll automático para o final

def iniciar_interface_servidor():
    # Função para iniciar a interface gráfica do servidor
    root = tk.Tk()
    tela_servidor = TelaServidor(root)

    # Entrada para o tempo de espera da IA
    label_tempo = tk.Label(root, text="Informe o tempo de espera para respostas da IA (em segundos):")
    label_tempo.grid(row=1, column=0, padx=10, pady=10)

    input_tempo = tk.Entry(root)
    input_tempo.grid(row=2, column=0, padx=10, pady=10)

    def start_server():
        """Função para iniciar o servidor com o tempo de espera da IA informado."""
        try:
            tempo_espera_ia = float(input_tempo.get())
            tela_servidor.inserir_texto(f"Tempo de espera configurado: {tempo_espera_ia} segundos")

            # Importar a função iniciar_servidor
            from tcp_server import iniciar_servidor

            # Iniciar o servidor em uma thread separada para não bloquear a interface
            server_thread = Thread(target=iniciar_servidor, args=(tempo_espera_ia, tela_servidor))
            server_thread.start()

        except ValueError:
            tela_servidor.inserir_texto("Erro: O tempo de espera deve ser um número.")

    # Botão para iniciar o servidor
    btn_iniciar = tk.Button(root, text="Iniciar Servidor", command=start_server)
    btn_iniciar.grid(row=3, column=0, padx=10, pady=10)

    # Inicia o loop da interface gráfica
    root.mainloop()
