import socket
import os
import threading
import hashlib

SERVIDOR = ""
PORTA = 2121
PASTA_ARQUIVOS = "arquivos"

#tamanhos
def adiciona_tamanho(dados):
    tamanho = len(dados)  # calcula tamanho em bytes
    return tamanho.to_bytes(4, byteorder='big') + dados

# Função para receber dados
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

#envia a lista de arquivos
def envia_lista_arquivos(sock_con):
    try:
        lista = os.listdir(PASTA_ARQUIVOS)
        resposta = ""
        for nome_arquivo in lista:
            caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo)
            if os.path.isfile(caminho):
                tamanho = os.path.getsize(caminho)
                resposta += f"{nome_arquivo} - {tamanho} bytes\r\n"
        dados = resposta.encode()
        sock_con.sendall(adiciona_tamanho(dados))
    except:
        sock_con.sendall(adiciona_tamanho(b""))

# Função para enviar o conteúdo de um arquivo ao cliente
def envia_arquivo(sock_con, nome_arquivo):
    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo.decode())
    if not os.path.isfile(caminho):
        sock_con.sendall((0).to_bytes(4, byteorder='big'))
        return
    try:
        with open(caminho, "rb") as f:
            conteudo = f.read()
            sock_con.sendall(adiciona_tamanho(conteudo))
    except:
        sock_con.sendall((0).to_bytes(4, byteorder='big'))

# Função para enviar hash MD5 
def envia_md5_parcial(sock_con, nome_arquivo, posicao_str):
    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo.decode())
    if not os.path.isfile(caminho):
        sock_con.sendall(adiciona_tamanho(b""))
        return
    try:
        posicao = int(posicao_str.decode())
        tamanho_arquivo = os.path.getsize(caminho)
        if posicao > tamanho_arquivo:
            posicao = tamanho_arquivo
        with open(caminho, "rb") as f:
            dados = f.read(posicao)
            md5 = hashlib.md5()
            md5.update(dados)
            hash_md5 = md5.hexdigest().encode()
            sock_con.sendall(adiciona_tamanho(hash_md5))
    except:
        sock_con.sendall(adiciona_tamanho(b""))

# Função para ler o que o cliente enviou
def le_comando(sock):
    dados = recebe_dados(sock)
    return dados

# Função que trata a conexão com o cliente
def trata_cliente(sock_con, endereco):
    try:
        while True:
            comando = le_comando(sock_con)
            if not comando:
                break

            if comando[:3] == b"DIR":
                envia_lista_arquivos(sock_con)

            elif comando[:3] == b"DOW":
                nome_arquivo = comando[4:]
                envia_arquivo(sock_con, nome_arquivo)

            elif comando[:3] == b"MD5":
                partes = comando.split(b" ")
                if len(partes) == 3:
                    nome_arquivo = partes[1]
                 

# Função principal para iniciar o servidor
def inicia_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((SERVIDOR, PORTA))
    servidor.listen()
    print(f"Servidor iniciado na porta {PORTA}...")
    while True:
        sock_con, endereco = servidor.accept()
        print(f"Conexão de {endereco}")
        thread = threading.Thread(target=trata_cliente, args=(sock_con, endereco))
        thread.start()

if __name__ == "__main__":
    inicia_servidor()
