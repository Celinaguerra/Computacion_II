import sys

# Muestra todos los argumentos
print("Todos los argumentos:", sys.argv)

# El primer argumento (índice 0) es siempre el nombre del script
print("Nombre del script:", sys.argv[0])

# Los siguientes son los argumentos pasados por el usuario
if len(sys.argv) > 1:
    print("Argumentos recibidos:", sys.argv[1:])
else:
    print("No se recibieron argumentos.")
