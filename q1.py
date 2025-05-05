# Converte 4 números (IP) para um número só de 32 bits
def juntar_ip(a, b, c, d):
    return (a << 24) | (b << 16) | (c << 8) | d

# Converte um número de 32 bits para 4 números (IP)
def separar_ip(ip):
    a = (ip >> 24) & 255
    b = (ip >> 16) & 255
    c = (ip >> 8) & 255
    d = ip & 255
    return a, b, c, d

# Calcula potências 
def potencia(base, expoente):
    resultado = 1
    for i in range(expoente):
        resultado = resultado * base
    return resultado


def main():
    # Entrada do usuário: 4 partes do IP e a máscara
    print("Digite o endereço IP:")
    a = int(input("Primeiro número (ex: 192): "))
    b = int(input("Segundo número (ex: 168): "))
    c = int(input("Terceiro número (ex: 1): "))
    d = int(input("Quarto número (ex: 10): "))
    
    bits = int(input("Digite a máscara em bits (ex: 24): "))

    # Junta o IP em um número só
    ip = juntar_ip(a, b, c, d)

    # Cria a máscara com 1s à esquerda e 0s à direita
    mascara = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF

    # Endereço de rede 
    rede = ip & mascara

    # Broadcast = IP OR (inverso da máscara)
    broadcast = ip | (~mascara & 0xFFFFFFFF)

    # Gateway = último IP antes do broadcast
    if broadcast > rede + 1:
        gateway = broadcast - 1
    else:
        gateway = 0  # Não aplicável

    # Número de hosts 
    host_bits = 32 - bits
    if host_bits > 0:
        hosts = potencia(2, host_bits) - 2
    else:
        hosts = 0

    # Imprimi resultados 
    r1, r2, r3, r4 = separar_ip(rede)
    b1, b2, b3, b4 = separar_ip(broadcast)
    g1, g2, g3, g4 = separar_ip(gateway)

    print("\nEndereço da rede: ", r1, ".", r2, ".", r3, ".", r4)
    print("Endereço de broadcast: ", b1, ".", b2, ".", b3, ".", b4)
    if gateway != 0:
        print("Endereço de gateway: ", g1, ".", g2, ".", g3, ".", g4)
    else:
        print("Endereço de gateway: Não aplicável")
    print("Número de hosts válidos:", hosts)

# Roda o programa
main()
