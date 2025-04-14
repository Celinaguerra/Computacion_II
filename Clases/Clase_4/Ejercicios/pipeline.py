# Proceso A → escribe → Pipe1 → lee → Proceso B → escribe → Pipe2 → lee → Proceso C
# Proceso A genera una cadena de texto.

# Proceso B convierte la cadena a mayúsculas.

# Proceso C imprime el resultado.

import os

# Pipe 1: A → B
r1, w1 = os.pipe()

# Pipe 2: B → C
r2, w2 = os.pipe()

# Crear proceso A
pid_a = os.fork()

if pid_a == 0:
    # Proceso A
    os.close(r1)
    os.close(r2)
    os.close(w2)
    
    mensaje = b"Hola desde el proceso A"
    os.write(w1, mensaje)
    os.close(w1)
    os._exit(0)

else:
    # Crear proceso B desde el padre
    pid_b = os.fork()

    if pid_b == 0:
        # Proceso B
        os.close(w1)
        os.close(r2)

        recibido = os.read(r1, 100)
        mensaje_mayusculas = recibido.upper()
        os.close(r1)

        os.write(w2, mensaje_mayusculas)
        os.close(w2)
        os._exit(0)

    else:
        # Crear proceso C desde el padre
        pid_c = os.fork()

        if pid_c == 0:
            # Proceso C
            os.close(w1)
            os.close(r1)
            os.close(w2)

            recibido = os.read(r2, 100)
            print("Proceso C recibió:", recibido.decode())
            os.close(r2)
            os._exit(0)

        else:
            # Proceso padre original espera a los 3 hijos
            os.close(r1)
            os.close(w1)
            os.close(r2)
            os.close(w2)
            os.wait()
            os.wait()
            os.wait()
