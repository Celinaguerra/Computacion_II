import json
import hashlib

NOMBRE_ARCHIVO_BLOCKCHAIN = "blockchain.json"
NOMBRE_ARCHIVO_REPORTE = "reporte.txt"

def verificar_y_reportar():
    print(f"--- Iniciando Verificación y Reporte desde '{NOMBRE_ARCHIVO_BLOCKCHAIN}' ---")

    try:
        with open(NOMBRE_ARCHIVO_BLOCKCHAIN, 'r') as f:
            blockchain = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO_BLOCKCHAIN}'.")
        print("Asegúrese de ejecutar primero 'sistema_biometrico.py' para generarlo.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo '{NOMBRE_ARCHIVO_BLOCKCHAIN}' está corrupto o no es un JSON válido.")
        return

    prev_hash_calculado = "0" * 64
    bloques_corruptos = []
    
    for i, bloque in enumerate(blockchain):
        if bloque["prev_hash"] != prev_hash_calculado:
            print(f"El 'prev_hash' del bloque {i} no coincide con el hash del bloque anterior.")
            bloques_corruptos.append(i)
        
        datos_bloque = bloque["datos"]
        timestamp_bloque = bloque["timestamp"]
        
        contenido_para_hash = bloque["prev_hash"] + json.dumps(datos_bloque, sort_keys=True) + timestamp_bloque
        hash_recalculado = hashlib.sha256(contenido_para_hash.encode('utf-8')).hexdigest()
        
        if bloque["hash"] != hash_recalculado:
            print(f"El contenido del bloque {i} ha sido alterado. Los hashes no coinciden.")
            if i not in bloques_corruptos:
                bloques_corruptos.append(i)

        prev_hash_calculado = bloque["hash"]

    if not bloques_corruptos:
        print("La integridad de la cadena de bloques es CORRECTA.")
    else:
        print(f"Se encontraron inconsistencias en los bloques: {bloques_corruptos}")

    if not blockchain:
        print("La cadena de bloques está vacía. No se puede generar el reporte.")
        return
        
    total_bloques = len(blockchain)
    bloques_con_alerta = sum(1 for b in blockchain if b["alerta"])
    
    frecuencias = [b["datos"]["frecuencia"]["media"] for b in blockchain]
    presiones = [b["datos"]["presion"]["media"] for b in blockchain]
    oxigenos = [b["datos"]["oxigeno"]["media"] for b in blockchain]
    
    promedio_frecuencia = sum(frecuencias) / len(frecuencias) if frecuencias else 0
    promedio_presion = sum(presiones) / len(presiones) if presiones else 0
    promedio_oxigeno = sum(oxigenos) / len(oxigenos) if oxigenos else 0

    contenido_reporte = f"""
# REPORTE DE ANÁLISIS BIOMÉTRICO

## Resumen de la Cadena de Bloques
- Cantidad total de bloques: {total_bloques}
- Número de bloques con alertas: {bloques_con_alerta}
- Estado de integridad: {'CORRECTA' if not bloques_corruptos else f'FALLIDA (Bloques corruptos: {bloques_corruptos})'}

## Promedios Generales de la Prueba de Esfuerzo
- Promedio general de Frecuencia Cardíaca (media): {promedio_frecuencia:.2f} ppm
- Promedio general de Presión Sistólica (media): {promedio_presion:.2f} mmHg
- Promedio general de Saturación de Oxígeno (media): {promedio_oxigeno:.2f} %
"""

    with open(NOMBRE_ARCHIVO_REPORTE, 'w') as f:
        f.write(contenido_reporte.strip())

    print(f"\nReporte final generado en '{NOMBRE_ARCHIVO_REPORTE}'.")


if __name__ == "__main__":
    verificar_y_reportar()