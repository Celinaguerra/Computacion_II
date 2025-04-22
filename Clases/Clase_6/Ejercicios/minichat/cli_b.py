# import os

# fifo_write = "/tmp/fifo_B_A"
# fifo_read = "/tmp/fifo_A_B"

# if not os.path.exists(fifo_write):
#     os.mkfifo(fifo_write)
# if not os.path.exists(fifo_read):
#     os.mkfifo(fifo_read)

# # Leer mensaje
# with open(fifo_read, 'r') as fr:
#     mensaje = fr.readline().strip()
#     print("[B] Mensaje recibido de A:", mensaje)

# # Enviar respuesta
# with open(fifo_write, 'w') as fw:
#     respuesta = input("Escribe un mensaje para enviar a A: ")
#     fw.write(respuesta + "\n")
#     fw.flush()  # Asegúrate de que el mensaje se escriba inmediatamente


# #bucle infinito

import os

fifo_write = "/tmp/fifo_B_A"
fifo_read = "/tmp/fifo_A_B"

if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)
if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)

print("Cliente B listo. Escribí 'exit' para salir.")

while True:
    with open(fifo_read, 'r') as fr:
        mensaje = fr.readline().strip()
        print("A >", mensaje)

    if mensaje.lower() == "exit":
        break

    with open(fifo_write, 'w') as fw:
        respuesta = input("B > ")
        fw.write(respuesta + "\n")
        fw.flush()

    if respuesta.strip().lower() == "exit":
        break
