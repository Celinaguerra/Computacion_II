# TP2 - Sistema de Scraping

Este proyecto implementa un sistema distribuido (Partes A y B) para
scrapear y analizar sitios web.

## Estructura

-   `server_scraping.py`: Servidor A. Punto de
    entrada HTTP.
-   `server_processing.py`: Servidor B.
    Worker de tareas pesadas.
-   `client.py`: Cliente de prueba de línea de comandos.
-   `common/`: Módulos de protocolo y serialización.
-   `scraper/`: Módulos de lógica de scraping.
-   `processor/`: Módulos de lógica de procesamiento.
-   `tests/`: Pruebas unitarias.
-   `requirements.txt`: Dependencias.

## Dependencias

1.  Instalar dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

2.  Instalar el navegador para Playwright (necesario para el
    Servidor B):
    ```bash
    playwright install chromium
    ```


## Instrucciones de Ejecución

Debes correr los dos servidores en terminales separadas antes de
usar el cliente.

### 1. Iniciar Servidor B (Procesamiento)

Abre una terminal y ejecuta:


```bash
# IPv4
python3 server_processing.py -i 127.0.0.1 -p 9001

# IPv6
python3 server_processing.py -i ::1 -p 9001
```

### 2. Iniciar Servidor A (Scraping)
Abre otra terminal y ejecuta:

```bash
# IPv4
python3 server_scraping.py -i 127.0.0.1 -p 8000

# IPv6
python3 server_scraping.py -i :: -p 8000
```

### 3. Ejecutar el cliente
Abre otra terminal y utiliza client.py para hacer una solicitud:

```bash
# python client.py <ip_servidor_A> <puerto_servidor_A> <url_a_scrapear>

python3 client.py 127.0.0.1 8000 https://github.com
```

### 4. Testing
Sobre la carpeta "TP2" ejecuta el siguiente comando:

```bash
python3 -m pytest tests/test_scraper.py tests/test_processor.py
```