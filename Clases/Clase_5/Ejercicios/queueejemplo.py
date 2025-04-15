from multiprocessing import Process, Queue
import time

def productor(q):
    for i in range(5):
        mensaje = f"Mensaje {i}"
        print(f"[Productor] Enviando: {mensaje}")
        q.put(mensaje)
        time.sleep(1)  # Simula trabajo

def consumidor(q):
    for i in range(5):
        mensaje = q.get()
        print(f"[Consumidor] Recibido: {mensaje}")
        time.sleep(1.5)  # Simula trabajo más lento

if __name__ == '__main__':
    q = Queue()  # Creamos la cola compartida

    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Programa terminado.")
