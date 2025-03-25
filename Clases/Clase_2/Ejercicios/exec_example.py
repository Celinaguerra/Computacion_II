import os

print(f"Soy el proceso padre con PID {os.getpid()}")

pid = os.fork()

if pid == 0:
    print(f"Soy el hijo con PID {os.getpid()}, ejecutando 'ls -l'")
    os.execlp("ls", "ls", "-l")  # Reemplaza el proceso hijo con 'ls -l'
    print("Este mensaje nunca se imprimirá")  # exec reemplaza completamente el proceso
else:
    print(f"El padre {os.getpid()} creó al hijo {pid}")
