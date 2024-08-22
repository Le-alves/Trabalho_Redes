import socket
import random
import threading
import time

class Servidor:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"[*] Servidor escutando em {self.host}:{self.port}")

        self.modo = input("Escolha o modo de operação: 1 - Automático, 2 - Manual: ")
        self.tempo_espera = float(input("Defina o tempo de espera (em segundos): "))

    def gerar_respostas_fake(self, prompt):
        respostas = [
            "Isso parece interessante.",
            "Poderia me explicar melhor?",
            "Eu não tenho certeza sobre isso.",
            "Que ótimo ponto de vista!",
            "Vamos analisar isso mais a fundo."
        ]
        return random.choice(respostas)

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            if self.modo == '1':
                time.sleep(self.tempo_espera)
                resposta = self.gerar_respostas_fake(request)
            elif self.modo == '2':
                print(f"Pergunta recebida: {request}")
                resposta = input("Digite a resposta que você gostaria de enviar: ")

            client_socket.send(resposta.encode('utf-8'))

        client_socket.close()

    def start(self):
        print("[*] Aguardando conexão do cliente...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[*] Conexão aceita de {addr}")
            self.handle_client(client_socket)
            client_socket.close()


class Cliente:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
        except ConnectionRefusedError as e:
            print(f"Conexão recusada ao tentar conectar a {self.host}:{self.port}: {e}")
            raise
        except socket.gaierror as e:
            print(f"Erro ao resolver o endereço do host '{self.host}': {e}")
            raise
        except Exception as e:
            print(f"Erro ao conectar ao servidor no endereço '{self.host}:{self.port}': {e}")
            raise
        self.nome = ""
        self.acertos = 0
        self.total_perguntas = 0

    def registrar_nome(self):
        self.nome = input("Digite seu nome: ")
        self.client_socket.send(self.nome.encode('utf-8'))

    def fazer_pergunta(self):
        while True:
            message = input("Digite sua pergunta (ou 'sair' para encerrar): ")
            if message.lower() == 'sair':
                break

            self.client_socket.send(message.encode('utf-8'))
            response = self.client_socket.recv(4096).decode('utf-8')
            print(f"Resposta: {response}")

            self.total_perguntas += 1
            self.verificar_origem(response)

            nova_pergunta = input("Você deseja fazer uma nova pergunta? (s/n): ").lower()
            if nova_pergunta != 's':
                break

        self.mostrar_resumo()
        self.client_socket.close()

    def verificar_origem(self, resposta):
        origem = input("Você acha que a resposta é de um humano (h) ou IA (i)? ").lower()
        correta = 'i'  # Supondo que a resposta correta seja sempre IA
        if origem == 'h' or origem == 'i':
            if origem == correta:
                self.acertos += 1
                print("Você acertou!")
            else:
                print("Você errou!")
        else:
            print("Opção inválida, considere como erro.")

    def mostrar_resumo(self):
        print(f"\nResumo do Teste:\nTotal de perguntas: {self.total_perguntas}\nTotal de acertos: {self.acertos}\nTotal de erros: {self.total_perguntas - self.acertos}")


class TestSetup:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port

    def start_server(self):
        servidor = Servidor(self.host, self.port)
        server_thread = threading.Thread(target=servidor.start)
        server_thread.daemon = True
        server_thread.start()
        return server_thread

    def start_client(self):
        cliente = Cliente(self.host, self.port)
        cliente.registrar_nome()
        cliente.fazer_pergunta()

    def run_test(self):
        # Iniciar o servidor
        server_thread = self.start_server()
        # Esperar um tempo para garantir que o servidor está pronto
        time.sleep(2)
        # Iniciar o cliente
        self.start_client()


if __name__ == "__main__":
    test_setup = TestSetup()
    test_setup.run_test()
