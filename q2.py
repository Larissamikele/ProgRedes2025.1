import hashlib
import time

# Função para encontrar o nonce certo
def findNonce(dataToHash, bitsToBeZero):
    start_time = time.time()  # Marca o início

    nonce = 0  # Começamos com nonce 0

    # Quantos bytes e bits precisam ser 0
    total_bytes = bitsToBeZero // 8
    extra_bits = bitsToBeZero % 8

    while True:
        # Converte o nonce para 4 bytes (big-endian)
        nonce_bytes = nonce.to_bytes(4, byteorder='big')

        # Junta o nonce + dados
        full_input = nonce_bytes + dataToHash

        # Calcula o hash SHA-256
        hash_bytes = hashlib.sha256(full_input).digest()

        # Verifica se os primeiros bytes são zero
        all_zero = True
        for i in range(total_bytes):
            if hash_bytes[i] != 0:
                all_zero = False
                break

        # Se os bytes estão certos, verifica os bits restantes
        if all_zero and extra_bits > 0:
            next_byte = hash_bytes[total_bytes]
            mask = 0xFF << (8 - extra_bits) & 0xFF
            if next_byte & mask != 0:
                all_zero = False

        if all_zero:
            break  # Achou o nonce certo
        else:
            nonce += 1  # Tenta o próximo

    end_time = time.time()  # finaliza
    elapsed_time = end_time - start_time
    return nonce, hash_bytes.hex(), elapsed_time


# Função principal para testar diferentes textos e bits
def main():
    testes = [
        ("Esse um texto elementar", 8),
        ("Esse um texto elementar", 10),
        ("Esse um texto elementar", 15),
        ("Textinho", 8),
        ("Textinho", 18),
        ("Textinho", 22),
        ("Meu texto médio", 18),
        ("Meu texto médio", 19),
        ("Meu texto médio", 20)
    ]

    print(f"{'Texto':<25} {'Bits em zero':<14} {'Nonce':<10} {'Tempo (s)':<10}")
    print("-" * 60)

    for texto, bits in testes:
        dados = texto.encode('utf-8')  # Converte para bytes
        nonce, hash_final, tempo = findNonce(dados, bits)
        print(f"{texto:<25} {bits:<14} {nonce:<10} {tempo:.4f}")


# Roda o programa
if __name__ == "__main__":
    main()
