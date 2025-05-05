# Entrada dos dados
ip = input("Digite o endereço IP (ex: 192.168.1.10): ")
mascara_bits = int(input("Digite a máscara em bits (ex: 24): "))

# Dividindo o IP em pequenas partes
ip_partes = ip.split(".")
ip_numeros = [int(p) for p in ip_partes]

# Cria umas mascara em quatro partes
mascara = [0, 0, 0, 0]
for i in range(mascara_bits):
    bloco = i // 8
    bit = 7 - (i % 8)
    mascara[bloco] += 2 ** bit

# Endereço de rede = IP AND máscara
rede = []
for i in range(4):
    rede.append(ip_numeros[i] & mascara[i])

# Endereço de broadcast 
broadcast = []
for i in range(4):
    broadcast.append(ip_numeros[i] | (255 - mascara[i]))

# Gateway = último IP válido
gateway = broadcast[:]
if gateway[3] > 1:
    gateway[3] -= 1
else:
    if gateway[2] > 0:
        gateway[2] -= 1
        gateway[3] = 255
    else:
        gateway = ["Não aplicável"]

# Cálculo de hosts 
bits_host = 32 - mascara_bits
if bits_host > 0:
    total_hosts = (2 ** bits_host) - 2
else:
    total_hosts = 0

# Imprimi os resultados 
print("\nEndereço da rede:", ".".join(str(n) for n in rede))
print("Endereço de broadcast:", ".".join(str(n) for n in broadcast))
if gateway == ["Não aplicável"]:
    print("Endereço de gateway: Não aplicável")
else:
    print("Endereço de gateway:", ".".join(str(n) for n in gateway))
print("Número de hosts válidos:", total_hosts)
