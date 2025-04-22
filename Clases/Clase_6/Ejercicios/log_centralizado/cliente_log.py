# cliente_log.py
import time
fifo = "/tmp/log_fifo"

with open(fifo, 'w') as f:
    for i in range(3):
        f.write(f"Evento {i} desde cliente\n")
        f.flush()
        time.sleep(1)