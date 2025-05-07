# Nome da imagem
nome_arquivo = 'WhatsApp Image 2025-05-07 at 17.36.08.jpeg'

# 01 ETAPA: abrir e ler os primeiros 6 bytes
with open(nome_arquivo, 'rb') as f:
    primeiros_bytes = f.read(6)
    # Os bytes 4 e 5 estão nos índices 4 e 5
    byte4 = primeiros_bytes[4]
    byte5 = primeiros_bytes[5]
    # Calcula o tamanho dos metadados (big-endian)
    app1DataSize = (byte4 << 8) + byte5
    print(f"Tamanho de app1Data (app1DataSize): {app1DataSize} bytes")

# 02 ETAPA: abrir de novo e processar os metadados
with open(nome_arquivo, 'rb') as f:
    f.read(4)  # Ignora os primeiros 4 bytes
    app1Data = f.read(app1DataSize)  # Lê os metadados

    # Verifica se tem pelo menos 18 bytes para acessar a posição 16 (índice 16 e 17)
    if len(app1Data) >= 18:
        byte16 = app1Data[16]
        byte17 = app1Data[17]
        # Calcula número de metadados (big-endian)
        numero_metadados = (byte16 << 8) + byte17
        print(f"Número de metadados na imagem: {numero_metadados}")
    else:
        print("Não foi possível acessar a posição 16 de app1Data.")
