import socket       
import os           
import threading    
import hashlib      

SERVIDOR = ""     
PORTA = 2121       
PASTA_ARQUIVOS = 'arquivos'  

# Função que adiciona o tamanho dos dados no começo da mensagem
def adiciona_tamanho(dados):
    tamanho = len(dados)  # Calcula o tamanho dos dados em bytes
    
    return tamanho.to_bytes(4, byteorder='big') + dados

# Função para enviar a lista de arquivos ao cliente
def envia_lista_arquivos(sock_con):
    try:
        lista = os.listdir(PASTA_ARQUIVOS)  #lista dos arquivos
        resposta = ""
        for nome_arquivo in lista:
            caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo)  # Caminho completo do arquivo
            if os.path.isfile(caminho):  # Verifica se é um arquivo 
                tamanho = os.path.getsize(caminho)  
                # Adiciona nome e tamanho 
                resposta += f"{nome_arquivo} - {tamanho} bytes\r\n"
        dados = resposta.encode()  # Converte texto para bytes para enviar na rede
        sock_con.sendall(adiciona_tamanho(dados))  # Envia tamanho + dados para o cliente
    except:
        #para casos de erro
        sock_con.sendall(adiciona_tamanho(b""))

# Função para enviar o conteúdo de um arquivo para o cliente
def envia_arquivo(sock_con, nome_arquivo):
    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo.decode())  # Constrói o caminho completo do arquivo
    if not os.path.isfile(caminho):  # Se o arquivo não existir
        sock_con.sendall((0).to_bytes(4, byteorder='big')) 
        return
    try:
        with open(caminho, "rb") as f:  # Abre o arquivo em modo leitura binária
            conteudo = f.read()         
            sock_con.sendall(adiciona_tamanho(conteudo))  # Envia tamanho e o conteudo
    except:
        # Se der erro na leitura envia o 0
        sock_con.sendall((0).to_bytes(4, byteorder='big'))

#enviar o hash MD5 de parte do arquivo
def envia_md5_parcial(sock_con, nome_arquivo, posicao_str):
    caminho = os.path.join(PASTA_ARQUIVOS, nome_arquivo.decode())
    if not os.path.isfile(caminho):
        sock_con.sendall(adiciona_tamanho(b""))  # Envia vazio se arquivo não existir
        return
    try:
        posicao = int(posicao_str.decode())  #deixa o texto em número inteiro
        tamanho_arquivo = os.path.getsize(caminho)  
        if posicao > tamanho_arquivo:
            posicao = tamanho_arquivo  # Ajusta para não passar do tamanho do arquivo
        with open(caminho, "rb") as f:
            dados = f.read(posicao)  # Lê só até a posição pedida do arquivo
            md5 = hashlib.md5()      # Cria o objeto para calcular o MD5
            md5.update(dados)        # Calcula o hash MD5 dos dados lidos

            def trata_cliente(sock_con, endereco):
    try:
        while True:
            comando = le_comando(sock_con)  # Lê o comando enviado pelo cliente
            if not comando:
                break  # Se não recebeu nada, fecha conexão

            if comando[:3] == b"DIR":  # Se comando for 'DIR' - lista arquivos
                envia_lista_arquivos(sock_con)
            elif comando[:3] == b"DOW":  # Se comando for 'DOW' - download arquivo
                nome_arquivo = comando[4:
                                       
nome_arquivo = comando[4:]  # Pega o nome do arquivo que vem depois do 'DOW '
                envia_arquivo(sock_con, nome_arquivo)
            elif comando[:3] == b"MD5":  # Se comando for 'MD5' - hash parcial
                # Espera comando no formato: b"MD5 nome_arquivo posicao"
                partes = comando.split(b" ")
                if len(partes) == 3:
                    nome_arquivo = partes[1]
                    posicao_str = partes[2]
                    envia_md5_parcial(sock_con, nome_arquivo, posicao_str)
                else:
            hash_md5 = md5.hexdigest().encode()  # Pega o hash em texto e transforma em bytes
           if __name__ == "__main__":
    inicia_servidor()  