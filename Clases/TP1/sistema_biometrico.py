import os
import json
import time
import random
import hashlib
import numpy as np
from multiprocessing import Process, Pipe, Queue, Lock
from datetime import datetime

NUM_MUESTRAS = 60
VENTANA_SEGUNDOS = 30
NOMBRE_ARCHIVO_BLOCKCHAIN = "blockchain.json"

def generador_datos(pipe_frecuencia, pipe_presion, pipe_oxigeno, num_muestras):

    print(f"[GENERADOR] Iniciando simulación de {num_muestras} muestras.")
    for i in range(num_muestras):
        timestamp = datetime.now().isoformat()
        
        dato = {
            "timestamp": timestamp,
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],
            "oxigeno": random.randint(90, 100)
        }
        
        print(f"[GENERADOR] Muestra {i+1}/{num_muestras}: F={dato['frecuencia']}, P={dato['presion']}, O={dato['oxigeno']}%")

        pipe_frecuencia.send(dato)
        pipe_presion.send(dato)
        pipe_oxigeno.send(dato)
        
        time.sleep(1)

    print("[GENERADOR] Simulación finalizada. Enviando señales de cierre.")
    pipe_frecuencia.send(None)
    pipe_presion.send(None)
    pipe_oxigeno.send(None)

    pipe_frecuencia.close()
    pipe_presion.close()
    pipe_oxigeno.close()
    print("[GENERADOR] Proceso finalizado.")

def analizador(pipe_conn, cola_resultados, tipo_señal, ventana_segundos):
    """
    Recibe datos de un Pipe, mantiene una ventana móvil de los últimos N segundos,
    calcula estadísticas (media y desv. estándar) y envía el resultado a una Queue.
    """
    print(f"[ANALIZADOR {tipo_señal.upper()}] Proceso iniciado. PID: {os.getpid()}")
    ventana_datos = []

    while True:
        try:
            dato_recibido = pipe_conn.recv()

            if dato_recibido is None:
                print(f"[ANALIZADOR {tipo_señal.upper()}] Señal de fin recibida. Terminando.")
                break

            if tipo_señal == "presion":
                valor_señal = dato_recibido[tipo_señal][0] 
            else:
                valor_señal = dato_recibido[tipo_señal]
            
            ventana_datos.append(valor_señal)

            if len(ventana_datos) > ventana_segundos:
                ventana_datos.pop(0)

            media = np.mean(ventana_datos)
            desv_estandar = np.std(ventana_datos)

            resultado = {
                "tipo": tipo_señal,
                "timestamp": dato_recibido["timestamp"],
                "media": float(media),
                "desv": float(desv_estandar)
            }
            
            cola_resultados.put(resultado)

        except EOFError:
            print(f"[ANALIZADOR {tipo_señal.upper()}] Error: Pipe cerrado prematuramente.")
            break
            
    pipe_conn.close()
    print(f"[ANALIZADOR {tipo_señal.upper()}] Proceso finalizado.")


def verificador(cola_resultados, num_muestras, lock_archivo):

    print(f"[VERIFICADOR] Proceso iniciado. PID: {os.getpid()}. Esperando {num_muestras} bloques.")
    blockchain = []
    prev_hash = "0" * 64 

    for i in range(num_muestras):
        resultados_del_timestamp = {}
        while len(resultados_del_timestamp) < 3:
            resultado = cola_resultados.get()
            resultados_del_timestamp[resultado['tipo']] = resultado
        
        alerta = False
        if resultados_del_timestamp["frecuencia"]["media"] >= 200:
            alerta = True
        if not (90 <= resultados_del_timestamp["oxigeno"]["media"] <= 100):
            alerta = True
        if resultados_del_timestamp["presion"]["media"] >= 200:
            alerta = True

        timestamp_bloque = resultados_del_timestamp["frecuencia"]["timestamp"]
        
        datos_bloque = {
            "frecuencia": {"media": resultados_del_timestamp["frecuencia"]["media"], "desv": resultados_del_timestamp["frecuencia"]["desv"]},
            "presion": {"media": resultados_del_timestamp["presion"]["media"], "desv": resultados_del_timestamp["presion"]["desv"]},
            "oxigeno": {"media": resultados_del_timestamp["oxigeno"]["media"], "desv": resultados_del_timestamp["oxigeno"]["desv"]},
        }

        contenido_para_hash = prev_hash + json.dumps(datos_bloque, sort_keys=True) + timestamp_bloque
        
        hash_actual = hashlib.sha256(contenido_para_hash.encode('utf-8')).hexdigest()

        bloque = {
            "indice": i,
            "timestamp": timestamp_bloque,
            "datos": datos_bloque,
            "alerta": alerta,
            "prev_hash": prev_hash,
            "hash": hash_actual
        }

        blockchain.append(bloque)
        
        with lock_archivo:
            with open(NOMBRE_ARCHIVO_BLOCKCHAIN, 'w') as f:
                json.dump(blockchain, f, indent=4)

        print(f"[VERIFICADOR] Bloque {i} añadido. Hash: {hash_actual[:10]}... Alerta: {alerta}")

        prev_hash = hash_actual

    print(f"[VERIFICADOR] Proceso finalizado. Blockchain guardada en {NOMBRE_ARCHIVO_BLOCKCHAIN}")


if __name__ == "__main__":
    print("--- INICIANDO SISTEMA CONCURRENTE DE ANÁLISIS BIOMÉTRICO ---")

    cola_resultados = Queue()

    p_frec_lectura, p_frec_escritura = Pipe()
    p_pres_lectura, p_pres_escritura = Pipe()
    p_oxi_lectura, p_oxi_escritura = Pipe()

    lock_archivo = Lock()

    procesos = []

    p_generador = Process(target=generador_datos, 
                          args=(p_frec_escritura, p_pres_escritura, p_oxi_escritura, NUM_MUESTRAS))
    procesos.append(p_generador)

    p_analizador_frec = Process(target=analizador, 
                                args=(p_frec_lectura, cola_resultados, "frecuencia", VENTANA_SEGUNDOS))
    procesos.append(p_analizador_frec)

    p_analizador_pres = Process(target=analizador, 
                                args=(p_pres_lectura, cola_resultados, "presion", VENTANA_SEGUNDOS))
    procesos.append(p_analizador_pres)

    p_analizador_oxi = Process(target=analizador, 
                               args=(p_oxi_lectura, cola_resultados, "oxigeno", VENTANA_SEGUNDOS))
    procesos.append(p_analizador_oxi)

    p_verificador = Process(target=verificador, 
                            args=(cola_resultados, NUM_MUESTRAS, lock_archivo))
    procesos.append(p_verificador)


    for p in procesos:
        p.start()


    p_frec_escritura.close()
    p_pres_escritura.close()
    p_oxi_escritura.close()
    p_frec_lectura.close()
    p_pres_lectura.close()
    p_oxi_lectura.close()


    for p in procesos:
        p.join()

    print("--- SISTEMA FINALIZADO  ---")
