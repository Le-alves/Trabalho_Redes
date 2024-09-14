# tela_cliente.py
import tkinter as tk
from tkinter import messagebox, simpledialog

class TelaCliente:
    def __init__(self, root, cliente_gerenciador):
        self.cliente_gerenciador = cliente_gerenciador  # Referência à lógica de comunicação
        self.root = root
        self.root.title("Cliente - Teste de Turing")

        # Criar os elementos da interface
        self.criar_interface()

    def criar_interface(self):
        # Configura o layout com espaçamento
        self.root.columnconfigure(0, weight=1)  # Coluna 0
        self.root.columnconfigure(1, weight=1)  # Coluna 1

        # Label e entrada para nome do usuário
        self.label_nome = tk.Label(self.root, text="Digite seu nome para registro no servidor:")
        self.label_nome.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.input_nome = tk.Entry(self.root, width=50)
        self.input_nome.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.btn_registrar = tk.Button(self.root, text="Registrar", command=self.registrar_cliente)
        self.btn_registrar.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Caixa de texto para exibir a resposta do servidor
        self.output_texto = tk.Text(self.root, height=10, width=50)
        self.output_texto.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Botões do menu
        self.btn_pergunta = tk.Button(self.root, text="Fazer Pergunta", command=self.mostrar_pergunta, state='disabled')
        self.btn_pergunta.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.btn_sair = tk.Button(self.root, text="Sair", command=self.sair, state='disabled')
        self.btn_sair.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Campo de pergunta
        self.label_pergunta = tk.Label(self.root, text="Digite sua pergunta:", state='disabled')
        self.label_pergunta.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.input_pergunta = tk.Entry(self.root, width=50, state='disabled')
        self.input_pergunta.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.btn_enviar_pergunta = tk.Button(self.root, text="Enviar Pergunta", command=self.enviar_pergunta, state='disabled')
        self.btn_enviar_pergunta.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def registrar_cliente(self):
        nome = self.input_nome.get()  # Obtém o nome do campo de texto
        if nome:
            resposta = self.cliente_gerenciador.registrar_nome(nome)  # Registra o nome no servidor
            self.output_texto.insert(tk.END, resposta + "\n")  # Exibe a confirmação de registro
            messagebox.showinfo("Registro", "Cliente registrado com sucesso no servidor.")
            
            # Habilitar o menu após o registro
            self.mostrar_menu()
        else:
            messagebox.showwarning("Atenção", "Por favor, digite seu nome.")

    def mostrar_menu(self):
        # Habilita os botões "Fazer Pergunta" e "Sair"
        self.btn_pergunta.config(state='normal')
        self.btn_sair.config(state='normal')
        
        # Exibe o menu na área de texto
        menu_texto = (
            "\nMenu:\n"
            "1. Fazer pergunta\n"
            "2. Ver ranking\n"
            "3. Sair\n"
            "Escolha uma opção acima clicando no botão correspondente."
        )
        self.output_texto.insert(tk.END, menu_texto + "\n")

    def habilitar_menu(self):
        # Habilitar botões do menu e campo de pergunta
        self.btn_pergunta.config(state='normal')
        self.btn_sair.config(state='normal')
        self.label_pergunta.config(state='normal')
        self.input_pergunta.config(state='normal')
        self.btn_enviar_pergunta.config(state='normal')

    def mostrar_pergunta(self):
         #Exibe a instrução para o cliente digitar a pergunta
        self.output_texto.insert(tk.END, "\nVocê escolheu fazer uma pergunta\n")
        
        # Habilita o campo de pergunta e o botão "Enviar Pergunta"
        self.input_pergunta.config(state='normal')
        self.btn_enviar_pergunta.config(state='normal')

    def enviar_pergunta(self):
        pergunta = self.input_pergunta.get()  # Obtém a pergunta do campo de entrada
        if pergunta:
            # Envia a pergunta para o Cliente_Gerenciador e obtém a resposta
            resposta = self.cliente_gerenciador.fazer_pergunta(pergunta)
            
            # Exibe a resposta na caixa de texto da interface
            self.output_texto.insert(tk.END, f"Resposta do servidor: {resposta}\n")

            # Pergunta ao usuário se a resposta veio de humano ou IA
            origem = tk.simpledialog.askstring("Origem", "Você acha que a resposta veio de um humano ou de uma máquina? (Humano = 1 | Máquina = 2): ")

            if origem:
                # Envia a escolha de origem ao servidor
                self.cliente_gerenciador.socket.send(origem.encode('utf-8'))

                # Recebe o feedback do servidor
                feedback = self.cliente_gerenciador.socket.recv(self.cliente_gerenciador.BUFFER_SIZE).decode('utf-8')

                # Exibe o feedback do servidor
                self.output_texto.insert(tk.END, f"Feedback: {feedback}\n")
        else:
            messagebox.showwarning("Atenção", "Digite uma pergunta para enviar.")

    def sair(self):
        resposta = self.cliente_gerenciador.sair()
        self.output_texto.insert(tk.END, resposta + "\n")
        self.root.quit()
