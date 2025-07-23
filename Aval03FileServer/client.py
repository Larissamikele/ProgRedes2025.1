import socket
import os
import hashlib

# Configurações do cliente
SERVIDOR = '10.214.251.50'  # IP do servidor (troque pelo seu IP)
PORTA = 2121
PASTA_ARQUIVOS = 'arquivos'  # Onde os arquivos baixados serão salvos

# Cria a pasta para os downloads, se não existir
if not os.path.exists(PASTA_ARQUIVOS):
    os.mkdir(PASTA_ARQUIVOS)

# Envia um comando para o servidor, com tamanho na frente
def enviar_comando(soquete, comando_texto):
    comando_bytes = comando_texto.encode()
    tamanho = len(comando_bytes)
    soquete.send(tamanho.to_bytes(4, byteorder='big') + comando_bytes)

# Recebe uma mensagem do servidor (que tem 4 bytes no começo com o tamanho)
def receber_resposta(soquete):
    tamanho_bytes = soquete.recv(4)
    if not tamanho_bytes:
        return None
    tamanho = int.from_bytes(tamanho_bytes, byteorder='big')
    dados = b''
    while len(dados) < tamanho:
        parte = soquete.recv(tamanho - len(dados))
        if not parte:
            break
        dados += parte
    return dados

# Faz o comando DIR para listar arquivos no servidor
def listar_arquivos(soquete):
    enviar_comando(soquete, 'DIR')
    resposta = receber_resposta(soquete)
    if resposta:
        print("Arquivos no servidor:")
        print(resposta.decode())
    else:
        print("Erro ao receber lista de arquivos.")

# Faz o download de um arquivo pelo nome
def baixar_arquivo(soquete, nome_arquivo):
    enviar_comando(soquete, f'DOW{nome_arquivo}')
    # Primeiro o servidor envia 4 bytes com o tamanho do arquivo
    tamanho_bytes = soquete.recv(4)
    if not tamanho_bytes:
        print("Erro ao receber tamanho do arquivo.")
        return
    tamanho = int.from_bytes(tamanho_bytes, byteorder='big')
    if tamanho == 0:
        print("Arquivo não encontrado no servidor.")
        return

    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo)
    with open(caminho, 'wb') as arquivo:
        bytes_recebidos = 0
        while bytes_recebidos < tamanho:
            dados = soquete.recv(min(1024, tamanho - bytes_recebidos))
            if not dados:
                break
            arquivo.write(dados)
            bytes_recebidos += len(dados)
    print(f"Download do arquivo '{nome_arquivo}' concluído!")

# Pede o hash MD5 parcial de um arquivo até uma posição
def pedir_md5(soquete, nome_arquivo, ate_posicao):
    comando = f'MD5{nome_arquivo}|{ate_posicao}'
    enviar_comando(soquete, comando)
    resposta = receber_resposta(soquete)
    if resposta:
        print(f"Hash MD5 parcial até {ate_posicao} bytes: {resposta.decode()}")
        return resposta.decode()
    else:
        print("Erro ao receber hash MD5.")
        return None

# Retoma o download (DRA)
def retomar_download(soquete, nome_arquivo):
    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo)
    if not os.path.exists(caminho):
        print("Arquivo local não existe para retomar download.")
        return

    tamanho_local = os.path.getsize(caminho)
    hash_local = calcular_md5_arquivo_parcial(caminho, tamanho_local)
    comando = f'DRA{nome_arquivo}|{tamanho_local}|{hash_local}'
    enviar_comando(soquete, comando)

    with open(caminho, 'ab') as arquivo:  # Abre para adicionar no final
        while True:
            dados = soquete.recv(1024)
            if not dados:
                break
            arquivo.write(dados)

    print(f"Download retomado do arquivo '{nome_arquivo}' finalizado.")

# Calcula o hash MD5 parcial do arquivo local
def calcular_md5_arquivo_parcial(caminho, ate_bytes):
    with open(caminho, 'rb') as arquivo:
        dados = arquivo.read(ate_bytes)
        return hashlib.md5(dados).hexdigest()

# Programa principal do cliente
def principal():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soquete:
        try:
            soquete.connect((SERVIDOR, PORTA))
            print("Conectado ao servidor.")

            while True:
                print("\nComandos disponíveis:")
                print("1 - Listar arquivos (DIR)")
                print("2 - Baixar arquivo (DOW)")
                print("3 - Pedir hash MD5 parcial (MD5)")
                print("4 - Retomar download (DRA)")
                print("0 - Sair")
