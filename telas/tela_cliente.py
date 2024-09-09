import tkinter as tk
from tkinter import messagebox
import socket
import threading
import os
import sys

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
            
            # Receber a resposta de boas-vindas do servidor
            resposta = self.socket_cliente.recv(1024).decode('utf-8')
            self.mostrar_mensagem(resposta)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar: {e}")
    
    def mostrar_mensagem(self, mensagem):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, mensagem + '\n')
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    cliente_interface = ClienteInterface(root)
    root.mainloop()
