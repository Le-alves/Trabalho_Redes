# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"
import tkinter as tk
from tela_cliente import TelaCliente
import socket, sys
from cliente_Gerenciador import Cliente_Gerenciador

HOST = '127.0.0.1'  # Endereço IP
PORT = 20000        # Porta utilizada pelo servidor
import tkinter as tk



def iniciar_interface():
    root = tk.Tk()
    cliente_gerenciador = Cliente_Gerenciador()  # Inicializa a lógica de comunicação
    app = TelaCliente(root, cliente_gerenciador)  # Passa o gerenciador para a interface gráfica
    root.mainloop()  # Inicia a interface gráfica

if __name__ == "__main__":
    iniciar_interface()
