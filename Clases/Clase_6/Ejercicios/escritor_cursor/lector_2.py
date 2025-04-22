# lector2.py
fifo = "/tmp/fifo_cursor"

with open(fifo, 'r') as f:
    contenido = f.read()
    print("[Lector 2] Leído:\n", contenido)
