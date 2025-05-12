# Nome da imagem
nome_arquivo = 'imagem_teste.jpeg'

# Abrir e ler os primeiros 6 bytes
with open(nome_arquivo, 'rb') as f:
    primeiros_bytes = f.read(6)
    # Os bytes 4 e 5 estão nos índices 4 e 5
    byte4 = primeiros_bytes[4]
    byte5 = primeiros_bytes[5]
    # Calcula o tamanho dos metadados (big-endian)
    app1DataSize = (byte4 << 8) + byte5
    print(f"Tamanho de app1Data (app1DataSize): {app1DataSize} bytes")

# Abrir de novo e processar os metadados
with open(nome_arquivo, 'rb') as f:
    f.read(4)  # Ignora os primeiros 4 bytes
    app1Data = f.read(app1DataSize)  # Lê os metadados

    if len(app1Data) >= 18:
        # Extrai número de metadados (posição 16 e 17)
        byte16 = app1Data[16]
        byte17 = app1Data[17]
        numero_metadados = (byte16 << 8) + byte17
        print(f"Número de metadados na imagem: {numero_metadados}")

        # Identificar os metadados e extrair a largura 
        inicio_metadados = 18  # Início dos metadados

        for i in range(numero_metadados):
            pos = inicio_metadados + i * 12  # Cada metadado tem 12 bytes

            if pos + 12 > len(app1Data):
                print("Fim dos dados atingido antes de completar todos os metadados.")
                break

            # Lê os campos do metadado
            tag = (app1Data[pos] << 8) + app1Data[pos + 1]           # 2 bytes
            tipo = (app1Data[pos + 2] << 8) + app1Data[pos + 3]      # 2 bytes
            qtd = int.from_bytes(app1Data[pos + 4:pos + 8], 'big')   # 4 bytes
            valor_ou_offset = int.from_bytes(app1Data[pos + 8:pos + 12], 'big')  # 4 bytes

            # Verifica se é a tag de largura ou altura
            if tag == 0x0100:  # Largura
                if qtd == 1 and tipo == 4:
                    print(f"Largura da imagem: {valor_ou_offset} pixels")
            elif tag == 0x0101:  # Altura
                if qtd == 1 and tipo == 4:
                    print(f"Altura da imagem: {valor_ou_offset} pixels")
      
    else:
        print("Não foi possível acessar a posição 16 de app1Data.")