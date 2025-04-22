# /tmp/chat_A_bus
# /tmp/chat_B_bus
# /tmp/chat_C_bus

# /tmp/chat_bus_A
# /tmp/chat_bus_B
# /tmp/chat_bus_C


import os

usuarios = ["A", "B", "C"]

for u in usuarios:
    fifo_in = f"/tmp/chat_{u}_bus"
    fifo_out = f"/tmp/chat_bus_{u}"
    for fifo in [fifo_in, fifo_out]:
        if not os.path.exists(fifo):
            os.mkfifo(fifo)
