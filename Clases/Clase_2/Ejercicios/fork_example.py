import os

print(f"Soy el proceso padre con PID {os.getpid()}")

pid = os.fork()  # Crear un nuevo proceso

if pid == 0:
    # Código que ejecuta el proceso hijo
    print(f"Soy el proceso hijo con PID {os.getpid()} y mi padre es {os.getppid()}")
else:
    # Código que ejecuta el proceso padre
    print(f"El proceso padre {os.getpid()} creó al hijo {pid}")
