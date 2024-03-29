import socket
import os

# Configurações do servidor
server_host = "127.0.0.1"
server_port = 12345


def enviar_arquivo(nome_arquivo, diretorio_destino):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Caminho completo do arquivo
    arquivo = os.path.join(os.getcwd(), nome_arquivo)

    # Conecta ao servidor
    client_socket.connect((server_host, server_port))

    # Tamanho do arquivo
    tamanho_arquivo = os.path.getsize(arquivo)

    # Envia o comando e o nome do arquivo
    mensagem = "enviar_arquivo {} {} {}".format(
        nome_arquivo, diretorio_destino, tamanho_arquivo)

    client_socket.send(mensagem.encode())

    # Lê o conteúdo do arquivo e envia em blocos
    with open(arquivo, 'rb') as file:
        for dados in iter(lambda: file.read(4096), b""):
            client_socket.sendall(dados)

    # Recebe a resposta do servidor
    resposta = client_socket.recv(1024).decode()

    # Exibe a resposta
    print("Resposta do servidor:", resposta)

    # Fecha a conexão com o servidor
    client_socket.close()


# Função para se conectar ao servidor e enviar uma mensagem
def enviar_mensagem(mensagem):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    client_socket.connect((server_host, server_port))

    # Envia a mensagem para o servidor
    client_socket.send(mensagem.encode())

    # Recebe a resposta do servidor
    resposta = client_socket.recv(1024).decode()

    # Exibe a resposta
    print("Resposta do servidor:", resposta)

    # Fecha a conexão com o servidor
    client_socket.close()

# Função principal do cliente


def client():
    while True:
        # Exibe as opções disponíveis
        print("\nOpções:")
        print("1. Criar diretório")
        print("2. Remover diretório")
        print("3. Listar conteúdo de diretório")
        print("4. Criar arquivo")
        print("5. Mover arquivo")
        print("6. Remover arquivo")
        print("7. Enviar arquivo")
        print("8. Sair")

        # Lê a opção escolhida pelo usuário
        opcao = input("Escolha uma opção (1-8): ")

        if opcao == "1":
            diretorio = input("Digite o nome do diretório a ser criado: ")
            mensagem = "criar_diretorio {}".format(diretorio)
            enviar_mensagem(mensagem)

        elif opcao == "2":
            diretorio = input("Digite o nome do diretório a ser removido: ")
            mensagem = "remover_diretorio {}".format(diretorio)
            enviar_mensagem(mensagem)

        elif opcao == "3":
            diretorio = input("Digite o nome do diretório a ser listado: ")
            mensagem = "listar_diretorio {}".format(diretorio)
            enviar_mensagem(mensagem)

        elif opcao == "4":
            path = input(
                "Digite o nome do arquivo com caminho do arquivo a ser criado (ex, teste/teste.txt): ")
            mensagem = "criar_arquivo {}".format(path)
            enviar_mensagem(mensagem)

        elif opcao == "5":
            path_arquivo = input(
                "Digite o nome do arquivo a ser movido (com o caminho): ")
            diretorio_destino = input(
                "Digite o nome do diretório de destino: ")
            mensagem = "mover_arquivo {} {}".format(
                path_arquivo, diretorio_destino)
            enviar_mensagem(mensagem)

        elif opcao == "6":
            path_arquivo = input(
                "Digite o caminho com o nome do arquivo a ser removido: ")
            mensagem = "remover_arquivo {}".format(path_arquivo)
            enviar_mensagem(mensagem)

        elif opcao == "7":
            nome_arquivo = input(
                "Digite o nome do arquivo a ser enviado (diretorio atual): ")
            diretorio_destino = input(
                "Digite o nome do diretório de destino (dentro de server_files): ")
            enviar_arquivo(nome_arquivo, diretorio_destino)

        elif opcao == "8":
            break
        else:
            print("Opção inválida")


# Executa o cliente
client()
