# logger.py
fifo = "/tmp/log_fifo"

print("[Logger] Esperando mensajes...")

with open(fifo, 'r') as f:
    while True:
        linea = f.readline()
        if linea:
            print(f"[LOG] {linea.strip()}")
