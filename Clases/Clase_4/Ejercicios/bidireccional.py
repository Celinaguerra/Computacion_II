import os

# Pipe 1: A → B
r1, w1 = os.pipe()

# Pipe 2: B → A
r2, w2 = os.pipe()

pid = os.fork()

if pid == 0:
    # Proceso B
    os.close(w1)  # No escribe en pipe1
    os.close(r2)  # No lee de pipe2

    # Leer mensaje de A
    recibido = os.read(r1, 100)
    print("B recibió:", recibido.decode())

    # Procesar y responder
    respuesta = recibido[::-1]  # Invertir el mensaje
    os.write(w2, respuesta)

    os.close(r1)
    os.close(w2)
    os._exit(0)

else:
    # Proceso A
    os.close(r1)  # No lee de pipe1
    os.close(w2)  # No escribe en pipe2

    mensaje = b"Hola B, soy A"
    os.write(w1, mensaje)

    # Esperar respuesta
    respuesta = os.read(r2, 100)
    print("A recibió respuesta:", respuesta.decode())

    os.close(w1)
    os.close(r2)
    os.wait()
