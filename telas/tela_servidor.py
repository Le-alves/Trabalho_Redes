import sys
import os
from tkinter import simpledialog

# Atualize o sys.path para incluir o diretório da pasta controle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import signal
# Agora importe de controle.tcp_server
from controle.tcp_server import main as servidor_main

import tkinter as tk
import threading

# Variável de controle para o servidor
servidor_ativo = True
escolha = None  # Variável global para armazenar a escolha
resposta = None  # Variável global para armazenar a resposta do humano
esperando_escolha = threading.Event()  # Evento para sincronização

# Função para iniciar o servidor
def iniciar_servidor(log_text_widget):
    global servidor_ativo
    servidor_ativo = True  # Ativa o servidor novamente, caso ele tenha sido parado

    # Função para rodar o servidor em uma thread separada
    def log(text):
        log_text_widget.insert(tk.END, text + "\n")  # Insere o log na área de texto
        log_text_widget.see(tk.END)  # Scroll automático para o final

    # Inicia o servidor normalmente como no seu código original, sem passar callbacks
    servidor_thread = threading.Thread(target=servidor_main, args=(log, escolha_callback, resposta_callback))
    servidor_thread.daemon = True  # Marca a thread como daemon para encerrar com a janela
    servidor_thread.start()
    log_text_widget.insert(tk.END, "Servidor iniciado...\n")

# Função para encerrar o servidor
def encerrar_servidor(log_text_widget):
    global servidor_ativo
    servidor_ativo = False  # Muda o estado do servidor para inativo
    log_text_widget.insert(tk.END, "Servidor encerrado.\n")
    log_text_widget.see(tk.END)

# Função para sair do programa
def sair_do_programa():
    os._exit(0)  # Força o encerramento de todo o programa


                #Funções para os botões de Humano e Ia 
def exibir_botoes_escolha():
    humano_button.pack(pady=5)  # Mostra o botão
    ia_button.pack(pady=5)      # Mostra o botão

def escolha_callback():
    exibir_botoes_escolha()  # Exibe os botões "IA" e "Humano"
    esperando_escolha.wait()  # Espera até que uma escolha seja feita
    return escolha  # Retorna a escolha feita (IA ou Humano)

def resposta_callback():
    return resposta  # Retorna a resposta que o humano digitar



# Função para configurar a interface do servidor
def criar_interface_servidor():
    global escolha, resposta, humano_button, ia_button
    root = tk.Tk()
    root.title("Servidor do Teste de Turing")
    root.geometry("400x400")

    # Adiciona um rótulo (texto informativo)
    label = tk.Label(root, text="Servidor está pronto para iniciar")
    label.pack(pady=20)

    # Adiciona a área de texto para exibir os logs do servidor
    log_text = tk.Text(root, height=10, width=50)
    log_text.pack(pady=10)

    # Função chamada ao clicar no botão "Iniciar Servidor"
    def iniciar_servidor_interface():
        label.config(text="Servidor em execução...")
        iniciar_servidor(log_text)

    # Funções chamadas quando o operador escolhe quem responde
    def escolher_ia():
        global escolha
        escolha = "IA"
        log_text.insert(tk.END, "IA foi selecionada para responder\n")
        humano_button.pack_forget()  # Esconde o botão
        ia_button.pack_forget()      # Esconde o botão
        esperando_escolha.set()  # Libera a execução do servidor

    def escolher_humano():
        global escolha, resposta
        escolha = "Humano"
        resposta = simpledialog.askstring("Resposta", "Digite a resposta para o cliente:")
        log_text.insert(tk.END, f"Humano foi selecionado. Resposta: {resposta}\n")
        humano_button.pack_forget()  # Esconde o botão
        ia_button.pack_forget()      # Esconde o botão
        esperando_escolha.set()  # Libera a execução do servidor

    # Botão para iniciar o servidor
    iniciar_button = tk.Button(root, text="Iniciar Servidor", command=iniciar_servidor_interface)
    iniciar_button.pack(pady=10)

    # Botões para fazer a escolha (Humano ou IA) - inicialmente escondidos
    humano_button = tk.Button(root, text="Humano", command=escolher_humano)
    ia_button = tk.Button(root, text="IA", command=escolher_ia)

    # Esconde os botões inicialmente
    humano_button.pack_forget()
    ia_button.pack_forget()

    # Botão para encerrar o servidor
    encerrar_button = tk.Button(root, text="Encerrar Servidor", command=lambda: encerrar_servidor(log_text))
    encerrar_button.pack(pady=10)

    # Captura o fechamento da janela e encerra o servidor
    root.protocol("WM_DELETE_WINDOW", sair_do_programa)

    root.mainloop()

if __name__ == "__main__":
    criar_interface_servidor()