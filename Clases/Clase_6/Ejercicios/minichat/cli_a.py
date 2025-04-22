# import os

# fifo_write = "/tmp/fifo_A_B"
# fifo_read = "/tmp/fifo_B_A"

# if not os.path.exists(fifo_write):
#     os.mkfifo(fifo_write)
# if not os.path.exists(fifo_read):
#     os.mkfifo(fifo_read)

# # Enviar mensaje
# with open(fifo_write, 'w') as fw:
#     mensaje = input("Escribe un mensaje para enviar a B: ")
#     fw.write(mensaje + "\n")
#     fw.flush()  # Asegúrate de que el mensaje se escriba inmediatamente

# # Leer respuesta
# with open(fifo_read, 'r') as fr:
#     respuesta = fr.readline().strip()
#     print("[A] Mensaje recibido de B:", respuesta)


###bucle infinito

import os

fifo_write = "/tmp/fifo_A_B"
fifo_read = "/tmp/fifo_B_A"

if not os.path.exists(fifo_write):
    os.mkfifo(fifo_write)
if not os.path.exists(fifo_read):
    os.mkfifo(fifo_read)

print("Cliente A listo. Escribí 'exit' para salir.")

while True:
    with open(fifo_write, 'w') as fw:
        mensaje = input("A > ")
        fw.write(mensaje + "\n")
        fw.flush()

    if mensaje.strip().lower() == "exit":
        break

    with open(fifo_read, 'r') as fr:
        respuesta = fr.readline().strip()
        print("B >", respuesta)

    if respuesta.lower() == "exit":
        break
