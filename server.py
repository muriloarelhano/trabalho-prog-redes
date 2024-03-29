import socket
import os
import logging

# Diretório base onde os arquivos serão armazenados
base_dir = "server_files"

# Função para listar o conteúdo de um diretório


def listar_diretorio(diretorio):
    path = os.path.join(base_dir, diretorio)
    conteudo = os.listdir(path)
    return "Conteúdo do diretório {}: {}".format(diretorio, conteudo)

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


# Função para criar um arquivo
def criar_arquivo(path):
    arquivo = os.path.join(base_dir, path)
    with open(arquivo, 'w') as file:
        pass  # Não é necessário escrever conteúdo no arquivo neste exemplo
    return "Arquivo criado com sucesso: {}".format(path)

# Função para mover um arquivo


def mover_arquivo(path_origem, path_destino):
    arquivo_origem = os.path.join(base_dir, path_origem)

    file_name, file_extension = os.path.splitext(os.path.basename(path_origem))

    arquivo_destino = os.path.join(
        base_dir, path_destino, file_name+file_extension)

    os.rename(arquivo_origem, arquivo_destino)

    return "Arquivo enviado com sucesso para o diretório {}: {}".format(path_destino, path_origem)

# Função para remover um arquivo


def remover_arquivo(path_arquivo):
    arquivo = os.path.join(base_dir, path_arquivo)
    os.remove(arquivo)
    return "Arquivo removido com sucesso: {}".format(path_arquivo)

# Função para enviar um arquivo a partir da raiz do terminal


def receber_arquivo(nome_arquivo, diretorio_destino, tamanho_arquivo, client_socket):
    # Caminho completo do arquivo
    arquivo = os.path.join(base_dir, diretorio_destino, nome_arquivo)

    # Lê o conteúdo do arquivo em blocos
    conteudo = b""
    bytes_recebidos = 0

    while bytes_recebidos < tamanho_arquivo:
        # Define o tamanho do bloco a ser recebido (4096 bytes)
        tamanho_bloco = min(4096, tamanho_arquivo - bytes_recebidos)
        bloco = client_socket.recv(tamanho_bloco)
        conteudo += bloco
        bytes_recebidos += len(bloco)

    # Salva o conteúdo do arquivo em disco
    with open(arquivo, 'wb') as file:
        file.write(conteudo)

    return "Arquivo {} salvo com sucesso!".format(nome_arquivo)

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

            elif comando == "criar_arquivo":
                resposta = criar_arquivo(argumento)

            elif comando == "mover_arquivo":
                origem, destino = argumento.split(" ", 1)
                resposta = mover_arquivo(origem, destino)

            elif comando == "enviar_arquivo":
                print(argumento.split(" "))

                nome_arquivo, diretorio_destino, tamanho_arquivo,  = argumento.split(
                    " ")

                tamanho_arquivo = int(tamanho_arquivo)

                resposta = receber_arquivo(
                    nome_arquivo, diretorio_destino, tamanho_arquivo, client_socket)

                print("Recebendo o arquivo...")
            elif comando == "remover_arquivo":
                resposta = remover_arquivo(argumento)

        except:
            resposta = "Erro ao executar o comando, provavelmente o diretório é invalido..."
            logging.exception(resposta)

        # Envia a resposta para o cliente
        client_socket.send(resposta.encode())

        # Fecha a conexão com o cliente
        client_socket.close()


if __name__ == "__main__":
    server()
