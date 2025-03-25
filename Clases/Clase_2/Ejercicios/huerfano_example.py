import os
import time

pid = os.fork()

if pid == 0:
    print(f"Soy el hijo {os.getpid()}, mi padre es {os.getppid()}")
    time.sleep(5)  # El hijo sigue vivo por 5 segundos
    print(f"Ahora mi padre es {os.getppid()}")  # Debería ser 1 (init)
else:
    print(f"Soy el padre {os.getpid()}, terminando ahora")
    exit(0)  # El padre termina antes que el hijo
