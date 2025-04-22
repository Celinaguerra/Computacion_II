import os
import sys

if len(sys.argv) != 2:
    print("Uso: python usuario.py <nombre>")
    sys.exit(1)

usuario = sys.argv[1]
fifo_in = f"/tmp/chat_bus_{usuario}"
fifo_out = f"/tmp/chat_{usuario}_bus"

if not os.path.exists(fifo_in) or not os.path.exists(fifo_out):
    print("Los FIFOs no existen. Corré setup_fifos.py primero.")
    sys.exit(1)

print(f"[{usuario}] Conectado al chat. Escribí mensajes. Ctrl+C para salir.")

# Abrir en modo lectura no bloqueante (escuchar mensajes del bus)
fifo_lectura = open(fifo_in, 'r')
fifo_envio = open(fifo_out, 'w')

try:
    while True:
        mensaje = input(f"[{usuario}] > ")
        fifo_envio.write(mensaje + "\n")
        fifo_envio.flush()
        
        # Leer lo que otros dijeron
        while True:
            recibido = fifo_lectura.readline()
            if recibido:
                print(recibido.strip())
            else:
                break

except KeyboardInterrupt:
    print(f"\n[{usuario}] Cerrando chat.")
    fifo_envio.close()
    fifo_lectura.close()
