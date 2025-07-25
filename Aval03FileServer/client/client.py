import socket
import os

SERVIDOR = "localhost"
PORTA = 2121

#adiciona o tamanho no inicio
def adiciona_tamanho(dados):
    tamanho = len(dados)
    return tamanho.to_bytes(4, 'big') + dados

#dados + tamanho
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

#peder a lista de arquivos ao servidor
def lista_arquivos(sock):
    comando = b"DIR"
    sock.sendall(adiciona_tamanho(comando))
    resposta = recebe_dados(sock)
    if resposta:
        print("Arquivos no servidor:")
        print(resposta.decode())
    else:
        print("Não foi possível obter a lista de arquivos.")

#download
def download_arquivo(sock):
    nome = input("Digite o nome do arquivo para baixar: ")
    comando = ("DOW " + nome).encode()
    sock.sendall(adiciona_tamanho(comando))
    dados = recebe_dados(sock)
    if not dados:
        print("Arquivo não encontrado.")
        return
    #Cria a pasta 'arquivos' se não existir
    if not os.path.exists("arquivos"):
        os.makedirs("arquivos")
    with open(os.path.join("arquivos", nome), "wb") as f:
        f.write(dados)
    print(f"Download do arquivo '{nome}' finalizado!")

#solicita hash MD5
def md5_parcial(sock):
    nome = input("Nome do arquivo para MD5 parcial: ")
    pos = input("Até qual posição (número) do arquivo?: ")
    comando = ("MD5 " + nome + " " + pos).encode()
    sock.sendall(adiciona_tamanho(comando))
    resposta = recebe_dados(sock)
    if resposta:
        print(f"Hash MD5 parcial do arquivo '{nome}' até posição {pos}: {resposta.decode()}")
    else:
        print("Erro ao obter hash MD5 do arquivo.")

#interface do cliente
def menu(sock):
    while True:
        print("\n===== Menu =====")
        print("1 - Listar arquivos")
        print("2 - Download de arquivo")
        print("3 - Obter hash MD5 parcial")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            lista_arquivos(sock)
        elif opcao == "2":
            download_arquivo(sock)
        elif opcao == "3":
            md5_parcial(sock)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVIDOR, PORTA))
            print(f"Conectado ao servidor {SERVIDOR}:{PORTA}")
            menu(sock)
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor. Verifique se ele está rodando e tente novamente.")

if __name__ == "__main__":
    main()
