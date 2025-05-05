def findNonce(dataToHash, bitsToBeZero):
    nonce = 0
    tentativas = 0  # Contador de tentativas para simular o tempo

    while True:
        # Junta o nonce com os dados (usando XOR)
        entrada = dataToHash ^ nonce

        # Gera um "hash" simples (não é SHA-256, é uma simulação simples)
        hash = entrada
        hash = hash ^ (hash >> 13)
        hash = hash ^ (hash << 5)
        hash = hash ^ (hash >> 7)
        hash = hash & 0xFFFFFFFF  # Garante que o hash tenha 32 bits

        # Conta quantos bits zero há no início do hash
        zeros = 0
        for i in range(31, -1, -1):  # Verifica cada bit a partir do mais significativo
            if (hash >> i) & 1 == 0:  # Se o bit for zero
                zeros += 1
            else:
                break  # Se encontrar um bit 1, para a contagem

        # Se o número de zeros for suficiente, encontramos o nonce correto
        if zeros >= bitsToBeZero:
            tempo_simulado = tentativas / 1_000_000  # Simula o tempo em segundos
            return nonce, hash, tempo_simulado

        # Incrementa o nonce e tenta novamente
        nonce += 1
        tentativas += 1
