import json

def serialize(data: dict) -> bytes:
    try:
        return json.dumps(data).encode('utf-8')
    except TypeError as e:
        print(f"Error de serialización: {e}. Asegúrate de que los datos sean compatibles con JSON.")
        # Manejo de error: serializa un error
        return json.dumps({"error": f"Datos no serializables: {e}"}).encode('utf-8')

def deserialize(data_bytes: bytes) -> dict:
    try:
        return json.loads(data_bytes.decode('utf-8'))
    except json.JSONDecodeError:
        print("Error: No se pudo decodificar el mensaje JSON recibido.")
        return {"error": "Mensaje JSON corrupto o mal formado"}