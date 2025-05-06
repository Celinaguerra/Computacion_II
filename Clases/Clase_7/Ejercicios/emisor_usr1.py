# emisor_usr1.py
import os
import signal
import time

# Cambiá esto al PID que imprime receptor_usr1.py
pid_objetivo = int(input("Ingresá el PID del receptor: "))

print(f"[INFO] Enviando SIGUSR1 a PID {pid_objetivo}...")
os.kill(pid_objetivo, signal.SIGUSR1)
