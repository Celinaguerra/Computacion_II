import os

# Crear el pipe
r, w = os.pipe()

# Crear un proceso hijo
pid = os.fork()

if pid == 0:
    # Proceso hijo
    os.close(r)  # No necesita leer
    mensaje = b"Mensaje desde el hijo"
    os.write(w, mensaje)
    os.close(w)
else:
    # Proceso padre
    os.close(w)  # No necesita escribir
    recibido = os.read(r, 100)
    print("Padre recibió:", recibido.decode())
    os.close(r)
