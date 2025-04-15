# Crear dos productores que envían mensajes al mismo consumidor.

# El consumidor debe procesarlos todos en orden de llegada.

# Al final, cada productor enviará su propio "FIN".

from multiprocessing import Process, Queue
import time

# prod 1
def productor1(q):
    for i in range(5):
        mensaje = f"Evento número {i}"
        print(f"[P1] Enviando: {mensaje}")
        q.put(mensaje)
        time.sleep(0.5)  # Simula producción de eventos

    q.put("FIN1")  # Señal de fin

# prod 2
def productor2(q):
    for i in range(5):
        mensaje = f"Evento número {i}"
        print(f"[P2] Enviando: {mensaje}")
        q.put(mensaje)
        time.sleep(1)  # Simula producción de eventos

    q.put("FIN2")  # Señal de fin

# consumidor
def consumidor(q):
    fines = 0
    while True:
        mensaje = q.get()
        if mensaje.startswith("FIN"):
            print(f"[Consumidor] Recibido: {mensaje}.")
            fines += 1
            if fines == 2:
                print("[Consumidor] Fin recibido. Terminando...")
                break
        else:
            print(f"[Consumidor] Guardando: {mensaje}")
            time.sleep(1)  # Simula procesamiento más lento

# 🚀 Código principal
if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=productor1, args=(q,))
    p2 = Process(target=productor2, args=(q,))
    p3 = Process(target=consumidor, args=(q,))


    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


    print("Procesos finalizados.")