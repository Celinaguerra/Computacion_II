# lector1.py
fifo = "/tmp/fifo_cursor"

with open(fifo, 'r') as f:
    contenido = f.read()
    print("[Lector 1] Leído:\n", contenido)
