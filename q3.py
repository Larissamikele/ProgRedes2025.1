# Nome do arquivo JPEG
nome_arquivo = 'imagem_teste.jpeg'

# Parte 1: Abrir o arquivo e ler os primeiros 6 bytes
with open(nome_arquivo, 'rb') as f:
    primeiros_bytes = f.read(6)

    # Verifica se conseguimos ler os 6 bytes
    if len(primeiros_bytes) < 6:
        print("Erro: Não foi possível ler os primeiros 6 bytes do arquivo.")
        exit()

    # Os bytes 4 e 5 contêm o tamanho dos metadados (app1DataSize)
    byte4 = primeiros_bytes[4]
    byte5 = primeiros_bytes[5]
    # Calcula o tamanho dos metadados (big-endian)
    app1DataSize = (byte4 << 8) + byte5
    print(f"Tamanho de app1Data (app1DataSize): {app1DataSize} bytes")

# Parte 2: Abrir novamente e processar os metadados
with open(nome_arquivo, 'rb') as f:
    f.read(4)  # Ignora os primeiros 4 bytes (identificador JPEG)
    app1Data = f.read(app1DataSize)  # Lê os metadados

    # Verifique se os dados lidos têm tamanho suficiente para continuar
    print(f"Tamanho de app1Data lido: {len(app1Data)} bytes")
    
    if len(app1Data) < 18:
        print("Erro: Dados insuficientes para ler os metadados.")
        print(f"Tamanho de app1Data lido: {len(app1Data)} bytes. Esperado: pelo menos 18 bytes.")
        exit()

    # Extrai o número de metadados (posição 16 e 17)
    byte16 = app1Data[16]
    byte17 = app1Data[17]
    numero_metadados = (byte16 << 8) + byte17
    print(f"Número de metadados: {numero_metadados}")

    # Inicializando variáveis para largura e altura
    largura = None
    altura = None

    # Identificar os metadados e extrair a largura e altura
    i = 18  # Início dos metadados
    for _ in range(numero_metadados):
        if i + 12 > len(app1Data):  # Se não houver dados suficientes para um metadado completo
            print("Erro: Não há dados suficientes para um metadado completo.")
            break

        # Lê os campos do metadado
        tag = (app1Data[i] << 8) + app1Data[i + 1]           # 2 bytes para tag
        tipo = (app1Data[i + 2] << 8) + app1Data[i + 3]      # 2 bytes para tipo
        qtd = (app1Data[i + 4] << 24) + (app1Data[i + 5] << 16) + (app1Data[i + 6] << 8) + app1Data[i + 7]  # 4 bytes para quantidade
        valor_ou_offset = (app1Data[i + 8] << 24) + (app1Data[i + 9] << 16) + (app1Data[i + 10] << 8) + app1Data[i + 11]  # 4 bytes para valor ou offset

        # Verifica se é a tag de largura (0x0100) ou altura (0x0101)
        if tag == 0x0100:  # Largura
            if qtd == 1 and tipo == 4:  # Tipo 4 é unsigned long
                largura = valor_ou_offset
                print(f"Largura da imagem: {largura} pixels")
        elif tag == 0x0101:  # Altura
            if qtd == 1 and tipo == 4:  # Tipo 4 é unsigned long
                altura = valor_ou_offset
                print(f"Altura da imagem: {altura} pixels")

        # Avança para o próximo metadado (12 bytes por metadado)
        i += 12

    # Verificar se encontramos as informações de largura e altura
    if largura is None:
        print("Erro: Largura não encontrada nos metadados.")
    if altura is None:
        print("Erro: Altura não encontrada nos metadados.")
