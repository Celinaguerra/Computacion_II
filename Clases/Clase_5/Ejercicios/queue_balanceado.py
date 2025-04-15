from multiprocessing import Process, Queue, current_process
import time
import random

def productor(q):
    for i in range(10):
        evento = f"Evento {i}"
        print(f"[Productor] Enviando: {evento}")
        q.put(evento)
        time.sleep(0.2)
    
    # Mandamos 1 señal de fin por consumidor
    for _ in range(3):
        q.put("FIN")

def consumidor(q):
    while True:
        mensaje = q.get()
        if mensaje == "FIN":
            print(f"[{current_process().name}] Recibió FIN. Cerrando.")
            break
        print(f"[{current_process().name}] Procesando: {mensaje}")
        time.sleep(random.uniform(0.5, 1.5))  # Simula procesamiento variable

if __name__ == '__main__':
    cola = Queue()
    
    p = Process(target=productor, args=(cola,))
    consumidores = [Process(target=consumidor, args=(cola,), name=f"Consumidor-{i+1}") for i in range(3)]
    
    p.start()
    for c in consumidores:
        c.start()

    p.join()
    for c in consumidores:
        c.join()

    print("✅ Todos los procesos finalizaron.")
