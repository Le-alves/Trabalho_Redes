import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time

class TelaServidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Teste de Turing")

        # Configura o grid para organizar melhor os widgets
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Campo para informar o tempo de espera da IA
        self.label_tempo = tk.Label(self.root, text="Informe o tempo de espera para IA:", font=('Arial', 12, 'bold'))
        self.label_tempo.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.input_tempo = tk.Entry(self.root, font=('Arial', 12))
        self.input_tempo.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        self.btn_iniciar = tk.Button(self.root, text="Iniciar", command=self.iniciar_servidor, bg='green', fg='white', font=('Arial', 12, 'bold'))
        self.btn_iniciar.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Caixa de texto para exibir logs
        self.output_texto = scrolledtext.ScrolledText(self.root, height=15, width=60, font=('Courier', 12))
        self.output_texto.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Botões de escolha: Humano ou IA
        self.label_escolha = tk.Label(self.root, text="Quem deve responder?", font=('Arial', 12, 'bold'))
        self.label_escolha.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.botao_humano = tk.Button(self.root, text="Humano", command=self.escolher_humano, state='disabled', font=('Arial', 12, 'bold'))
        self.botao_humano.grid(row=2, column=1, padx=10, pady=5)

        self.botao_ia = tk.Button(self.root, text="IA", command=self.escolher_ia, state='disabled', font=('Arial', 12, 'bold'))
        self.botao_ia.grid(row=2, column=2, padx=10, pady=5)

        # Campo de entrada para a resposta manual do operador
        self.label_resposta = tk.Label(self.root, text="Digite a resposta:", font=('Arial', 12, 'bold'), state='disabled')
        self.label_resposta.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.input_resposta = tk.Entry(self.root, font=('Arial', 12), state='disabled')
        self.input_resposta.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="e")

        # Botão para enviar a resposta
        self.botao_enviar_resposta = tk.Button(self.root, text="Enviar Resposta", command=self.enviar_resposta, state='disabled', bg='gray', fg='white', font=('Arial', 12, 'bold'))
        self.botao_enviar_resposta.grid(row=4, column=2, padx=10, pady=10, sticky="e")

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Aguardando", font=('Arial', 12), fg='red')
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        # Variáveis de controle
        self.gerenciador_atual = None
        self.quem_responde = None
        self.pergunta_atual = ""

    def iniciar_servidor(self):
        # Iniciar servidor
        self.status_label.config(text="Servidor iniciado", fg='green')
        self.inserir_texto("Servidor foi iniciado com sucesso.")

    def exibir_pergunta(self, pergunta, gerenciador):
        """Exibe a pergunta recebida e permite escolher quem responde."""
        self.pergunta_atual = pergunta
        self.gerenciador_atual = gerenciador
        self.inserir_texto(f"Pergunta: {pergunta}")
        self.root.title(f"Servidor - Pergunta: {pergunta[:30]}...")  # Atualiza o título com a pergunta

        # Habilita os botões de escolha
        self.botao_humano.config(state='normal')
        self.botao_ia.config(state='normal')

    def escolher_humano(self):
        """Define que o Humano vai responder."""
        self.quem_responde = "Humano"
        self.label_resposta.config(state='normal')
        self.input_resposta.config(state='normal')
        self.botao_enviar_resposta.config(state='normal')
        self.status_label.config(text="Modo: Humano", fg='blue')

    def escolher_ia(self):
        """Define que a IA vai responder."""
        self.quem_responde = "IA"
        self.label_resposta.config(state='disabled')
        self.input_resposta.config(state='disabled')
        self.botao_enviar_resposta.config(state='normal')
        self.status_label.config(text="Modo: IA", fg='orange')

    def enviar_resposta(self):
        """Envia a resposta ao Server_Gerenciador."""
        if self.quem_responde == "Humano":
            resposta = self.input_resposta.get()
            self.gerenciador_atual.receber_resposta("Humano", resposta)
            self.inserir_texto(f"Resposta do humano: {resposta}")
            self.status_label.config(text="Resposta enviada (Humano)", fg='blue')
        else:
            resposta = self.gerenciador_atual.ia_resposta.gerar_resposta(self.pergunta_atual)
            self.gerenciador_atual.receber_resposta("IA", resposta)
            self.inserir_texto(f"Resposta da IA: {resposta}")
            self.status_label.config(text="Resposta enviada (IA)", fg='orange')

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
    root.mainloop()
