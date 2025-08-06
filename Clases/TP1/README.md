# Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local

Este proyecto implementa un sistema distribuido en procesos que simula y analiza datos biométricos de una prueba de esfuerzo en tiempo real, utilizando los conceptos de programación concurrente de Python (multiprocessing). Los resultados se validan y almacenan de forma segura en una cadena de bloques.

---

### Arquitectura
El sistema se compone de los siguientes procesos:

- Proceso Principal (Generador): Simula 60 muestras de datos biométricos (1 por segundo) y las envía a los procesos de análisis.

- Procesos de Análisis (Frecuencia, Presión, Oxígeno): Cada uno recibe los datos, calcula estadísticas sobre una ventana móvil de 30 segundos y envía un resultado.

- Proceso Verificador: Recibe los tres resultados analizados, los valida, construye un bloque con ellos y lo añade a una cadena de bloques en el archivo blockchain.json.

La comunicación se realiza mediante:

- Pipes: Para enviar datos desde el Generador a cada Analizador.

- Queue: Para que los Analizadores envíen sus resultados al Verificador de forma segura.

 ----

### Archivos del Proyecto
- sistema_biometrico.py: El script principal que lanza la simulación y construye la cadena de bloques.

- verificar_cadena.py: Un script externo para verificar la integridad del archivo blockchain.json y generar un reporte final en reporte.txt.

- blockchain.json: (Generado) El archivo que contiene la cadena de bloques con los resultados del análisis.

- reporte.txt: (Generado) Un informe resumido con las estadísticas de la simulación.

----

### Requisitos
- Python 3.9 o superior

- Librería numpy:

    ```bash
    pip install numpy
    ```

---

### Instrucciones de Ejecución

El proyecto debe ejecutarse en dos pasos y en el orden correcto:

**Paso 1:**

Abre una terminal en el directorio del proyecto y ejecuta el siguiente comando. Esto iniciará el sistema concurrente, simulará los 60 segundos de la prueba de esfuerzo y generará el archivo blockchain.json.
```bash 
python3 sistema_biometrico.py
```
Verás en la consola la salida de cada proceso a medida que se generan y procesan los datos.

**Paso 2:**

Una vez que el primer script haya finalizado, ejecuta el script de verificación. Este leerá blockchain.json, comprobará que no haya sido alterado y creará el archivo reporte.txt.
```
python verificar_cadena.py
```
La salida te informará si la cadena es íntegra y confirmará la creación del reporte.
