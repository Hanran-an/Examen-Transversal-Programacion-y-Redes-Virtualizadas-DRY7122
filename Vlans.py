entrada = input("Ingresa un número de VLAN: ")
numero = int(entrada)

if numero >= 1 and numero <= 1005:
    print("VLAN normal")
elif numero >= 1006 and numero <= 4094:
    print("VLAN extendida")
else:
    print("El número ingresado no es válido")