import socket

# Função para se conectar ao servidor e enviar uma mensagem


def enviar_mensagem(mensagem):
    # Configurações do servidor
    server_host = "127.0.0.1"
    server_port = 12345

    # Cria um socket TCP/IP
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
        print("4. Enviar arquivo")
        print("5. Remover arquivo")
        print("6. Sair")

        # Lê a opção escolhida pelo usuário
        opcao = input("Escolha uma opção (1-6): ")

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
            nome_arquivo = input("Digite o nome do arquivo a ser enviado: ")
            diretorio_destino = input(
                "Digite o nome do diretório de destino: ")
            mensagem = "enviar_arquivo {} {}".format(
                nome_arquivo, diretorio_destino)
            enviar_mensagem(mensagem)
        elif opcao == "5":
            nome_arquivo = input("Digite o nome do arquivo a ser removido: ")
            diretorio = input("Digite o nome do diretório do arquivo: ")
            mensagem = "remover_arquivo {} {}".format(nome_arquivo, diretorio)
            enviar_mensagem(mensagem)
        elif opcao == "6":
            break
        else:
            print("Opção inválida")


# Executa o cliente
client()
