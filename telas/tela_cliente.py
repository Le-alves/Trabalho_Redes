import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import threading
import os
import sys
import select  # Importa o módulo select para verificar a disponibilidade de dados no socket

# Adiciona o diretório pai ao sys.path para incluir o diretório 'controle'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controle.cliente_Gerenciador import Cliente_Gerenciador

class ClienteInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente - Máquina de Turing")
        
        # Campo de entrada para o nome do usuário
        self.label = tk.Label(root, text="Digite seu nome:")
        self.label.pack(pady=10)
        
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack(pady=10)
        
        # Botão para conectar ao servidor
        self.btn_conectar = tk.Button(root, text="Conectar", command=self.conectar)
        self.btn_conectar.pack(pady=10)
        
        # Área de texto para exibir as mensagens
        self.text_area = tk.Text(root, state='disabled', height=10, width=50)
        self.text_area.pack(pady=10)
        
        self.socket_cliente = None  # O socket do cliente será inicializado após a conexão
        self.gerenciador = None  # Instância de Cliente_Gerenciador será armazenada aqui
        self.thread_receber = None  # Para armazenar a thread de recebimento de mensagens

    def conectar(self):
        nome_usuario = self.entry_nome.get()
        if not nome_usuario:
            messagebox.showwarning("Erro", "Por favor, insira um nome.")
            return
        
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.connect(('127.0.0.1', 20000))  # IP e Porta do servidor
            self.mostrar_mensagem(f"Conectado ao servidor como {nome_usuario}")
            
            # Enviar o nome do usuário ao servidor
            self.socket_cliente.send(nome_usuario.encode('utf-8'))

            # Cria a instância do Cliente_Gerenciador
            self.gerenciador = Cliente_Gerenciador(self.socket_cliente,self.mostrar_mensagem, self.callback_origem)

            # Receber a resposta de boas-vindas do servidor
            resposta = self.socket_cliente.recv(1024).decode('utf-8')
            self.mostrar_mensagem(resposta)

            # Iniciar a thread para recebimento de mensagens em segundo plano
            self.thread_receber = threading.Thread(target=self.receber_mensagens, daemon=True)
            self.thread_receber.start()

            # Mostra o menu depois de conectar
            self.mostrar_menu()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar: {e}")

    def mostrar_menu(self):
        # Esconde os componentes de conexão
        self.label.pack_forget()
        self.entry_nome.pack_forget()
        self.btn_conectar.pack_forget()

        # Título do menu
        self.label_menu = tk.Label(self.root, text="Escolha uma opção:")
        self.label_menu.pack(pady=10)

        # Criar um frame para organizar os botões lado a lado
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Campo de entrada para a pergunta
        self.entry_pergunta = tk.Entry(self.root, width=50)
        self.entry_pergunta.pack(pady=5)

        # Botão "Fazer Pergunta" que envia a pergunta ao servidor
        self.btn_opcao1 = tk.Button(button_frame, text="Fazer pergunta", command=self.enviar_pergunta)
        self.btn_opcao1.grid(row=0, column=0, padx=5)

    def enviar_pergunta(self):
        # Captura o texto da pergunta inserido no campo de entrada
        pergunta = self.entry_pergunta.get()

        if not pergunta:
            messagebox.showwarning("Aviso", "A pergunta não pode estar vazia.")
            return

        if self.gerenciador:
            # Exibe a pergunta na área de texto
            self.mostrar_mensagem(f"Você: {pergunta}")

            # Envia a pergunta ao servidor
            self.gerenciador.fazer_pergunta(pergunta)

            # Limpa o campo de entrada após enviar a pergunta
            self.entry_pergunta.delete(0, tk.END)

    def callback_origem(self):
        # Abre uma caixa de diálogo para o usuário escolher se a resposta veio de um humano ou de uma máquina
        origem = simpledialog.askstring("Palpite", "Você acha que essa resposta veio de um humano ou de uma máquina? (Humano = 1 | Máquina = 2):")
        if origem not in ["1", "2"]:
            messagebox.showwarning("Aviso", "Por favor, insira '1' para Humano ou '2' para Máquina.")
            return None
        return origem


    def receber_mensagens(self):
        while True:
            try:
                # Usando select para verificar se há dados disponíveis no socket
                ready_to_read, _, _ = select.select([self.socket_cliente], [], [], 1)
                if ready_to_read:
                    resposta = self.socket_cliente.recv(1024).decode('utf-8')
                    if resposta:
                        # Exibe a resposta do servidor na área de texto
                        self.mostrar_mensagem(f"Servidor: {resposta}")
            except Exception as e:
                print(f"Erro ao receber mensagem do servidor: {e}")
                break

    def mostrar_mensagem(self, mensagem):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, mensagem + '\n')
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    cliente_interface = ClienteInterface(root)
    root.mainloop()
