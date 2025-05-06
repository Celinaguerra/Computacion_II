import signal
import os
import time

def manejador_sigint(signum, frame):
    print("\n[INFO] Recibí SIGINT (Ctrl+C). Finalizando de forma segura.")
    exit(0)

# Asociamos la señal SIGINT al manejador personalizado
signal.signal(signal.SIGINT, manejador_sigint)

print(f"[PID] Mi PID es {os.getpid()}. Presioná Ctrl+C para interrumpir.")

while True:
    time.sleep(1)
