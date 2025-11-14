import requests
import sys
import json

def main():
    if len(sys.argv) != 4:
        print(f"Uso: python {sys.argv[0]} <ip_servidor_A> <puerto_servidor_A> <url_a_scrapear>")
        print(f"Ejemplo: python {sys.argv[0]} 127.0.0.1 8000 https://github.com")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    url_to_scrape = sys.argv[3]
    
    target_url = f"http://{server_ip}:{server_port}/scrape"
    params = {"url": url_to_scrape}
    
    print(f"Contactando a {target_url} para scrapear {url_to_scrape}...")
    
    try:
        response = requests.get(target_url, params=params, timeout=90)
        
        # Lanzar error si el servidor A devolvió 4xx o 5xx
        response.raise_for_status()
        
        data = response.json()
        
        print("\n--- Respuesta JSON Recibida (Truncada) ---")
        
        if "processing_data" in data:
            if "screenshot" in data["processing_data"]:
                data["processing_data"]["screenshot"] = data["processing_data"]["screenshot"][:50] + "... (truncado)"
            if "thumbnails" in data["processing_data"]:
                data["processing_data"]["thumbnails"] = [
                    t[:50] + "... (truncado)" for t in data["processing_data"]["thumbnails"]
                ]
                
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if data.get("status") == "error":
            print("\n--- ¡La solicitud falló! ---")
            print(f"Mensaje del servidor: {data.get('message')}")

    except requests.exceptions.ConnectionError:
        print(f"Error: No se pudo conectar a {target_url}.")
        print("¿Está 'server_scraping.py' corriendo?")
    except requests.exceptions.Timeout:
        print("Error: La solicitud excedió el timeout de 90 segundos.")
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: El servidor devolvió el código {e.response.status_code}")
        try:
            print(f"Detalle: {e.response.json()}")
        except requests.JSONDecodeError:
            print(f"Detalle: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()