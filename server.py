import socket
import os
import logging

# Diretório base onde os arquivos serão armazenados
base_dir = "server_files"

# Função para criar um diretório


def criar_diretorio(diretorio):
    path = os.path.join(base_dir, diretorio)
    os.makedirs(path)
    return "Diretório criado com sucesso: {}".format(diretorio)

# Função para remover um diretório


def remover_diretorio(diretorio):
    path = os.path.join(base_dir, diretorio)
    os.rmdir(path)
    return "Diretório removido com sucesso: {}".format(diretorio)

# Função para listar o conteúdo de um diretório


def listar_diretorio(diretorio):
    path = os.path.join(base_dir, diretorio)
    conteudo = os.listdir(path)
    return "Conteúdo do diretório {}: {}".format(diretorio, conteudo)

# Função para enviar um arquivo


def enviar_arquivo(nome_arquivo, diretorio_destino):
    arquivo_origem = os.path.join(base_dir, nome_arquivo)
    arquivo_destino = os.path.join(base_dir, diretorio_destino, nome_arquivo)
    os.rename(arquivo_origem, arquivo_destino)
    return "Arquivo enviado com sucesso para o diretório {}: {}".format(diretorio_destino, nome_arquivo)

# Função para remover um arquivo


def remover_arquivo(nome_arquivo, diretorio):
    arquivo = os.path.join(base_dir, diretorio, nome_arquivo)
    os.remove(arquivo)
    return "Arquivo removido com sucesso: {}".format(nome_arquivo)

# Função principal do servidor


def server():
    # Configurações do servidor
    host = "127.0.0.1"
    port = 12345

    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket ao host e porta
    server_socket.bind((host, port))

    # Escuta por conexões entrantes
    server_socket.listen(1)

    print("Servidor aguardando conexões...")

    while True:
        # Aguarda uma nova conexão
        client_socket, addr = server_socket.accept()
        print("Conexão estabelecida com: ", addr)

        # Recebe a mensagem do cliente
        mensagem = client_socket.recv(1024).decode()

        # Separa a mensagem em comando e argumento
        comando, argumento = mensagem.split(" ", 1)

        try:
            # Executa o comando solicitado pelo cliente
            if comando == "criar_diretorio":
                resposta = criar_diretorio(argumento)
            elif comando == "remover_diretorio":
                resposta = remover_diretorio(argumento)
            elif comando == "listar_diretorio":
                resposta = listar_diretorio(argumento)
            elif comando == "enviar_arquivo":
                nome_arquivo, diretorio_destino = argumento.split(" ", 1)
                resposta = enviar_arquivo(nome_arquivo, diretorio_destino)
        except:
            resposta = "Erro ao executar o comando, provavelmente o diretório é invalido..."
            logging.exception(resposta)

        # Envia a resposta para o cliente
        client_socket.send(resposta.encode())

        # Fecha a conexão com o cliente
        client_socket.close()


if __name__ == "__main__":
    server()