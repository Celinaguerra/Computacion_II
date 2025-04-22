import os

usuarios = ["A", "B", "C"]

# Abrir todos los FIFOs de entrada en modo lectura
fifo_inputs = {u: open(f"/tmp/chat_{u}_bus", 'r') for u in usuarios}
fifo_outputs = {u: open(f"/tmp/chat_bus_{u}", 'w') for u in usuarios}

print("[BUS] Esperando mensajes... (Ctrl+C para salir)")

try:
    while True:
        for u in usuarios:
            msg = fifo_inputs[u].readline()
            if msg:
                texto = f"[{u}] {msg.strip()}"
                print(texto)
                # reenviar a todos menos al emisor
                for target in usuarios:
                    if target != u:
                        fifo_outputs[target].write(texto + "\n")
                        fifo_outputs[target].flush()
except KeyboardInterrupt:
    print("\n[BUS] Cerrando...")
    for f in fifo_inputs.values():
        f.close()
    for f in fifo_outputs.values():
        f.close()
