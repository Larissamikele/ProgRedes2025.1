import socket


SERVIDOR = "localhost"
PORTA = 2121

# Função para adicionar o tamanho 
def adiciona_tamanho(dados):
    tamanho = len(dados)
    return tamanho.to_bytes(4, 'big') + dados

# Função para receber dados do servidor
def recebe_dados(sock):
    dados_tamanho = sock.recv(4)
    if len(dados_tamanho) < 4:
        return b""
    tamanho = int.from_bytes(dados_tamanho, 'big')
    dados = b""
    while tamanho > 0:
        parte = sock.recv(tamanho)
        if not parte:
            break
        dados += parte
        tamanho -= len(parte)
    return dados

# Função para pedir a lista de arquivos ao servidor
def lista_arquivos(sock):
    comando = b"DIR"
    sock.sendall(adiciona_tamanho(comando))
    resposta = recebe_dados(sock)
    print("Arquivos no servidor:")
    print(resposta.decode())

# Função para fazer download de arquivo
def download_arquivo(sock):
    nome = input("Digite o nome do arquivo para baixar: ")
    comando = ("DOW " + nome).encode()
    sock.sendall(adiciona_tamanho(comando))
    dados = recebe_dados(sock)
    if not dados:
        print("Arquivo não encontrado.")
        return
    with open("arquivos/" + nome, "wb") as f:
        f.write(dados)
    print("Download finalizado!")

# Função para obter hash MD5 parcial do arquivo
def md5_parcial(sock):
    nome = input("Nome do arquivo para MD5 parcial: ")
    pos = input("Até qual posição (número) do arquivo?: ")
   