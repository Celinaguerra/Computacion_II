import os

# Crear tres pipes
r1, w1 = os.pipe()  # A → B
r2, w2 = os.pipe()  # B → C
r3, w3 = os.pipe()  # C → A

pid_b = os.fork()

if pid_b == 0:
    # Proceso B
    os.close(w1)  # No escribe en pipe1
    os.close(r2)  # No lee de pipe2
    os.close(r3)  # No lee de pipe3
    os.close(w3)  # No escribe en pipe3

    mensaje = os.read(r1, 100)
    procesado = mensaje.upper()
    os.write(w2, procesado)

    os.close(r1)
    os.close(w2)
    os._exit(0)

pid_c = os.fork()
if pid_c == 0:
    # Proceso C
    os.close(r1)
    os.close(w1)
    os.close(w2)
    os.close(r3)

    mensaje = os.read(r2, 100)
    print("C recibió:", mensaje.decode())

    # Verificación: ¿el mensaje contiene "A"?
    if b"A" in mensaje:
        respuesta = b"Mensaje OK"
    else:
        respuesta = b"Mensaje invalido"

    os.write(w3, respuesta)

    os.close(r2)
    os.close(w3)
    os._exit(0)

# Proceso A (padre)
os.close(r1)
os.close(w2)
os.close(r2)
os.close(w3)

mensaje = b"hola desde A"
os.write(w1, mensaje)

respuesta = os.read(r3, 100)
print("A recibió de C:", respuesta.decode())

os.close(w1)
os.close(r3)

# Esperar hijos
os.wait()
os.wait()
