# ejercicio_basico.py
import signal
import os
import time

def manejador_sigint(signum, frame):
    print("\n[INFO] Recibí SIGINT (Ctrl+C). Terminando programa.")
    exit(0)

def manejador_sigterm(signum, frame):
    print("\n[INFO] Recibí SIGTERM (kill). Terminando programa.")
    exit(0)

# Asociar señales a manejadores
signal.signal(signal.SIGINT, manejador_sigint)
signal.signal(signal.SIGTERM, manejador_sigterm)

print(f"[PID] Mi PID es {os.getpid()}. Usá Ctrl+C o kill desde otra terminal.")

# Bucle infinito
while True:
    time.sleep(1)

##kill -TERM <PID>