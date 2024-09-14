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
        self.root.columnconfigure(2, weight=1)  # Coluna 2

        # Label e entrada para nome do usuário
        self.label_nome = tk.Label(self.root, text="Digite seu nome para registro no servidor:")
        self.label_nome.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.input_nome = tk.Entry(self.root, width=50)
        self.input_nome.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.btn_registrar = tk.Button(self.root, text="Registrar", command=self.registrar_cliente)
        self.btn_registrar.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # Caixa de texto para exibir a resposta do servidor
        self.output_texto = tk.Text(self.root, height=10, width=50)
        self.output_texto.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # Botões do menu: Colocando Fazer Pergunta, Ver Ranking, e Sair na mesma linha (linha 4)
        self.btn_pergunta = tk.Button(self.root, text="Fazer Pergunta", command=self.mostrar_pergunta, state='disabled')
        self.btn_pergunta.grid(row=4, column=0, padx=5, pady=5)  # Ajustando padx para controlar o espaço horizontal

        self.btn_ranking = tk.Button(self.root, text="Ver Ranking", command=self.ver_ranking, state='disabled')
        self.btn_ranking.grid(row=4, column=1, padx=5, pady=5)  # Ajustando padx para controlar o espaço horizontal

        self.btn_sair = tk.Button(self.root, text="Sair", command=self.sair, state='disabled')
        self.btn_sair.grid(row=4, column=2, padx=5, pady=5)  # Ajustando padx para controlar o espaço horizontal

        # Campo de pergunta
        self.label_pergunta = tk.Label(self.root, text="Digite sua pergunta:", state='disabled')
        self.label_pergunta.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        self.input_pergunta = tk.Entry(self.root, width=50, state='disabled')
        self.input_pergunta.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        self.btn_enviar_pergunta = tk.Button(self.root, text="Enviar Pergunta", command=self.enviar_pergunta, state='disabled')
        self.btn_enviar_pergunta.grid(row=7, column=0, columnspan=3, padx=10, pady=5)


    def ver_ranking(self):
        # Solicita o ranking ao Cliente_Gerenciador
        ranking = self.cliente_gerenciador.ver_ranking()

        # Exibe o ranking na caixa de texto da interface
        if ranking:
            self.output_texto.insert(tk.END, f"Ranking dos Usuários:\n{ranking}\n")
        else:
            self.output_texto.insert(tk.END, "Não foi possível obter o ranking.\n")
        
        self.output_texto.yview_moveto(1)  # Move a barra de rolagem para o final

        # Volta para o menu após exibir o ranking
        self.mostrar_menu()  # Aqui chamamos o menu de novo


    def registrar_cliente(self):
        nome = self.input_nome.get()  # Obtém o nome do campo de texto
        if nome:
            resposta = self.cliente_gerenciador.registrar_nome(nome)  # Registra o nome no servidor
            self.output_texto.insert(tk.END, resposta + "\n")  # Exibe a confirmação de registro
            messagebox.showinfo("Registro", "Cliente registrado com sucesso no servidor.")

            # Desabilitar o campo de nome após o registro
            self.input_nome.config(state='disabled')
            
            # Habilitar o menu após o registro
            self.mostrar_menu()
            self.btn_registrar.config(state='disabled')

        else:
            messagebox.showwarning("Atenção", "Por favor, digite seu nome.")

    def mostrar_menu(self):
        # Habilita os botões "Fazer Pergunta" e "Sair"
        self.btn_pergunta.config(state='normal')
        self.btn_ranking.config(state='normal')
        self.btn_sair.config(state='normal')

          # Desabilita o campo de pergunta e o botão "Enviar Pergunta"
        self.input_pergunta.config(state='disabled')
        self.btn_enviar_pergunta.config(state='disabled')
        
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

        # Desabilita os botões do menu enquanto a pergunta está sendo feita
        self.btn_pergunta.config(state='disabled')
        self.btn_ranking.config(state='disabled')
        self.btn_sair.config(state='disabled')

    def voltar_menu(self):
        # Desabilita o campo de pergunta e o botão "Enviar Pergunta"
        self.input_pergunta.config(state='disabled')
        self.btn_enviar_pergunta.config(state='disabled')
        
        # Habilita novamente os botões do menu
        self.btn_pergunta.config(state='normal')
        self.btn_sair.config(state='normal')

        # Exibe uma mensagem informando que o usuário pode escolher outra opção
        self.output_texto.insert(tk.END, "\nEscolha outra ação no menu.\n")

    def enviar_pergunta(self):
        pergunta = self.input_pergunta.get()  # Obtém a pergunta do campo de entrada
        if pergunta:
            # Envia a pergunta para o Cliente_Gerenciador e obtém a resposta
            resposta = self.cliente_gerenciador.fazer_pergunta(pergunta)
            
            # Exibe a resposta na caixa de texto da interface
            self.output_texto.insert(tk.END, f"Resposta do servidor: {resposta}\n")

            # Limpa o campo de pergunta
            self.input_pergunta.delete(0, tk.END)

            # Loop de validação para aceitar apenas "1" ou "2"
            origem = None
            
            while origem not in ("1", "2"):
                origem = tk.simpledialog.askstring(
                    "Origem", 
                    "Você acha que a resposta veio de um humano ou de uma máquina? (Humano = 1 | Máquina = 2): "
                )
                
                if origem not in ("1", "2"):
                    messagebox.showerror("Entrada Inválida", "Por favor, insira '1' para humano ou '2' para máquina.")

            if origem:
                # Chama o método `fazer_pergunta` para enviar a escolha ao servidor
                feedback = self.cliente_gerenciador.fazer_pergunta(origem)

                # Exibe o feedback do servidor
                self.output_texto.insert(tk.END, f"Feedback: {feedback}\n")

            self.output_texto.yview_moveto(1)  # Move a barra de rolagem para o final
            
            # Volta para o menu após o feedback
            self.mostrar_menu()  # Aqui chamamos o menu de novo
        else:
            messagebox.showwarning("Atenção", "Digite uma pergunta para enviar.")

    def sair(self):
        # Envia a solicitação de encerramento ao servidor
        resposta = self.cliente_gerenciador.sair()

        # Exibe a resposta do servidor ou qualquer mensagem de erro
        self.output_texto.insert(tk.END, resposta + "\n")

        # Fecha a interface gráfica após encerrar a conexão
        self.root.quit()

    