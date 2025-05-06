# receptor_usr1.py
import signal
import os
import time

def manejador_usr1(signum, frame):
    print(f"[INFO] Recibí SIGUSR1. Ejecutando acción personalizada.")

signal.signal(signal.SIGUSR1, manejador_usr1)

print(f"[PID receptor] {os.getpid()} esperando señal SIGUSR1...")

while True:
    time.sleep(1)
