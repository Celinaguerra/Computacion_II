from multiprocessing import Process, Queue
import time

# 🛠 Función del PRODUCTOR
def productor(q):
    for i in range(10):
        mensaje = f"Evento número {i}"
        print(f"[Productor] Enviando: {mensaje}")
        q.put(mensaje)
        time.sleep(0.5)  # Simula producción de eventos

    q.put("FIN")  # Señal de fin

# 🛠 Función del CONSUMIDOR
def consumidor(q):
    with open("log.txt", "w") as archivo:
        while True:
            mensaje = q.get()
            if mensaje == "FIN":
                print("[Consumidor] Fin recibido. Terminando...")
                break
            print(f"[Consumidor] Guardando: {mensaje}")
            archivo.write(mensaje + "\n")
            archivo.flush()  # Asegura escritura inmediata
            time.sleep(1)  # Simula procesamiento más lento

# 🚀 Código principal
if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Procesos finalizados. Revisá el archivo log.txt.")
