import os
import time

pid = os.fork()

if pid == 0:
    print(f"Soy el hijo {os.getpid()}, terminando inmediatamente")
    exit(0)  # El hijo termina
else:
    print(f"Soy el padre {os.getpid()}, sin llamar a wait()")
    time.sleep(10)  # El padre sigue vivo, pero no recoge al hijo
