import os

# Crear el pipe
r, w = os.pipe()

# Escribir en el pipe
os.write(w, b'Hola desde el pipe')

# Leer del pipe
mensaje = os.read(r, 100)  # leer hasta 100 bytes
print("Mensaje leído:", mensaje.decode())

# Cerrar los extremos
os.close(r)
os.close(w)
