from multiprocessing import Process, Queue, current_process
import time

#### NO FUNCIONA
# productor 1
def productor1(q):
    for i in range(5):
        mensaje = f"[P1] Evento {i}"
        print(mensaje)
        q.put(mensaje)
        time.sleep(0.5)
    q.put("FIN1")

# productor 2
def productor2(q):
    for i in range(5):
        mensaje = f"[P2] Evento {i}"
        print(mensaje)
        q.put(mensaje)
        time.sleep(1)
    q.put("FIN2")

# consumidor
def consumidor(q, id_consumidor, fin_total):
    recibidos = set()

    while True:
        mensaje = q.get()
        if mensaje.startswith("FIN"):
            print(f"[C{id_consumidor}] Recibido: {mensaje}")
            recibidos.add(mensaje)
            if len(recibidos) == fin_total:
                break
        else:
            print(f"[C{id_consumidor}] Procesando: {mensaje}")
            time.sleep(1)  # procesamiento lento

# 🚀 Código principal
if __name__ == '__main__':
    q = Queue()

    productores = [
        Process(target=productor1, args=(q,)),
        Process(target=productor2, args=(q,))
    ]

    consumidores = [
        Process(target=consumidor, args=(q, 1, 2)),
        Process(target=consumidor, args=(q, 2, 2))
    ]

    # Iniciar todos
    for p in productores + consumidores:
        p.start()

    # Esperar todos
    for p in productores + consumidores:
        p.join()

    print("Sistema finalizado con múltiples consumidores.")
