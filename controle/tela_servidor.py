import time
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

class TelaServidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Teste de Turing")

        # Configura o grid para organizar melhor os widgets
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Campo para informar o tempo de espera da IA
        self.label_tempo = tk.Label(self.root, text="Informe o tempo de espera para IA:")
        self.label_tempo.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.input_tempo = tk.Entry(self.root)
        self.input_tempo.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        self.btn_iniciar = tk.Button(self.root, text="Iniciar", command=self.start_server)
        self.btn_iniciar.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Caixa de texto para exibir logs
        self.output_texto = scrolledtext.ScrolledText(self.root, height=15, width=60)
        self.output_texto.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Botões de escolha: Humano ou IA
        self.label_escolha = tk.Label(self.root, text="Quem deve responder?")
        self.label_escolha.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.botao_humano = tk.Button(self.root, text="Humano", command=self.escolher_humano, state='disabled')
        self.botao_humano.grid(row=2, column=1, padx=10, pady=5)

        self.botao_ia = tk.Button(self.root, text="IA", command=self.escolher_ia, state='disabled')
        self.botao_ia.grid(row=2, column=2, padx=10, pady=5)

        # Campo de entrada para a resposta manual do operador
        self.label_resposta = tk.Label(self.root, text="Digite a resposta:", state='disabled')
        self.label_resposta.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.input_resposta = tk.Entry(self.root, state='disabled')
        self.input_resposta.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="e")

        # Botão para enviar a resposta
        self.botao_enviar_resposta = tk.Button(self.root, text="Enviar Resposta", command=self.enviar_resposta, state='disabled')
        self.botao_enviar_resposta.grid(row=4, column=2, padx=10, pady=5, sticky="e")

        # Variáveis de controle
        self.gerenciador_atual = None
        self.quem_responde = None
        self.pergunta_atual = ""

    def exibir_pergunta(self, pergunta, gerenciador):
        """Exibe a pergunta recebida e habilita os botões de escolha."""
        self.pergunta_atual = pergunta
        self.gerenciador_atual = gerenciador
        self.inserir_texto(f"Pergunta recebida: {pergunta}")
        
        # Habilita os botões de escolha
        self.botao_humano.config(state='normal')
        self.botao_ia.config(state='normal')

    def escolher_humano(self):
        """Define que o Humano vai responder e habilita o campo de resposta."""
        self.quem_responde = "Humano"
        self.label_resposta.config(state='normal')
        self.input_resposta.config(state='normal')
        self.botao_enviar_resposta.config(state='normal')

        # Desabilita os botões de escolha
        self.botao_humano.config(state='disabled')
        self.botao_ia.config(state='disabled')

    def escolher_ia(self):
        """Define que a IA vai responder e habilita o botão para enviar."""
        self.quem_responde = "IA"

        # Desabilitar o campo de texto da resposta manual
        self.label_resposta.config(state='disabled')
        self.input_resposta.config(state='disabled')

        # Habilitar o botão "Enviar Resposta"
        self.botao_enviar_resposta.config(state='normal')

        # Desabilita os botões de escolha
        self.botao_humano.config(state='disabled')
        self.botao_ia.config(state='disabled')

    def enviar_resposta(self):
        """Envia a resposta ao cliente, seja do Humano ou da IA."""
        if self.quem_responde == "Humano":
            resposta = self.input_resposta.get()
            if resposta:
                self.inserir_texto(f"Resposta enviada: {resposta}")
                self.input_resposta.delete(0, tk.END)  # Limpar campo de resposta
                self.gerenciador_atual.receber_resposta(self.quem_responde, resposta)
            else:
                self.inserir_texto("Erro: Resposta vazia.")
                return  # Não prosseguir se a resposta estiver vazia
        elif self.quem_responde == "IA":
            self.inserir_texto("IA está gerando a resposta...")
            # Gerar a resposta real usando a classe IA_Resposta
            resposta = self.ia_resposta.gerar_resposta(self.pergunta_atual)
            time.sleep(self.gerenciador_atual.tempo_espera_ia)
            self.inserir_texto(f"Resposta da IA enviada: {resposta}")
            self.gerenciador_atual.receber_resposta(resposta, self.quem_responde)

        # Desabilitar os botões e campos após o envio
        self.botao_enviar_resposta.config(state='disabled')
        self.input_resposta.config(state='disabled')
        self.label_resposta.config(state='disabled')

        # Resetar a variável quem_responde
        self.quem_responde = None

    def inserir_texto(self, mensagem):
        """Método para inserir texto na interface gráfica."""
        self.output_texto.insert(tk.END, mensagem + "\n")
        self.output_texto.yview(tk.END)  # Scroll automático para o final

    def start_server(self):
        """Função para iniciar o servidor com o tempo de espera da IA informado."""
        try:
            tempo_espera_ia = float(self.input_tempo.get())
            self.inserir_texto(f"Tempo de espera configurado: {tempo_espera_ia} segundos")

            # Simular a inicialização do servidor com o tempo de espera
            from tcp_server import iniciar_servidor

            # Iniciar o servidor em uma thread separada para não bloquear a interface
            server_thread = Thread(target=iniciar_servidor, args=(tempo_espera_ia, self))
            server_thread.start()

        except ValueError:
            self.inserir_texto("Erro: O tempo de espera deve ser um número.")

def iniciar_interface_servidor():
    # Função para iniciar a interface gráfica do servidor
    root = tk.Tk()
    tela_servidor = TelaServidor(root)
    root.mainloop()

