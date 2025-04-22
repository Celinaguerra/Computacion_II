# escritor_cursor.py
fifo = "/tmp/fifo_cursor"

with open(fifo, 'w') as f:
    for i in range(5):
        f.write(f"Mensaje {i}\n")
        f.flush()  # Asegúrate de que el mensaje se escriba inmediatamente