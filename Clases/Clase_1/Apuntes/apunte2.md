# 📌 Apuntes sobre `getopt` y `argparse`

## **1️⃣ Argumentos de línea de comandos en Python**
Los programas en Python pueden recibir argumentos desde la terminal al ejecutarse, lo que permite modificar su comportamiento sin cambiar el código.

### **Ejemplo con `sys.argv`**
```python
import sys
print("Argumentos recibidos:", sys.argv)
```
📌 `sys.argv` es una lista donde:
- `sys.argv[0]` es el nombre del script.
- Los demás elementos son los argumentos pasados al ejecutarlo.

**Ejemplo de ejecución:**
```bash
python script.py hola mundo
```
**Salida:**
```
['script.py', 'hola', 'mundo']
```

---

## **2️⃣ Uso de `getopt` para manejar argumentos**
`getopt` permite procesar argumentos con opciones cortas (`-n`) y largas (`--nombre`).

### **Ejemplo con `getopt`**
```python
import getopt
import sys

opts, args = getopt.getopt(sys.argv[1:], "n:", ["nombre="])

for opt, arg in opts:
    if opt in ("-n", "--nombre"):
        print(f"Nombre: {arg}")
```

**Ejemplo de ejecución:**
```bash
python script.py -n Juan
```
**Salida:**
```
Nombre: Juan
```
📌 `getopt` requiere manejar manualmente errores y validaciones.

---

## **3️⃣ Uso de `argparse`: la mejor opción**
`argparse` es más avanzado y fácil de usar. Permite definir argumentos, validarlos y mostrar ayuda automática.

### **Ejemplo básico con `argparse`**
```python
import argparse

parser = argparse.ArgumentParser(description="Ejemplo de uso de argparse")
parser.add_argument("-n", "--nombre", required=True, help="Nombre del usuario")
args = parser.parse_args()

print(f"Hola, {args.nombre}")
```

**Ejemplo de ejecución:**
```bash
python script.py -n Juan
```
**Salida:**
```
Hola, Juan
```
📌 `argparse`:
✅ Valida argumentos automáticamente.
✅ Genera ayuda (`-h`) sin necesidad de código extra.
✅ Permite definir tipos (`int`, `float`, etc.).

---

## **4️⃣ Desafío: Manejo de archivos con `argparse`**

```python
import argparse

parser = argparse.ArgumentParser(description="Procesar archivos")
parser.add_argument("-i", "--input", required=True, help="Archivo de entrada")
parser.add_argument("-o", "--output", required=True, help="Archivo de salida")
args = parser.parse_args()

print(f"Archivo de entrada: {args.input}")
print(f"Archivo de salida: {args.output}")
```

**Ejemplo de ejecución:**
```bash
python procesar_archivo.py -i datos.txt -o salida.txt
```
**Salida:**
```
Archivo de entrada: datos.txt
Archivo de salida: salida.txt
```

---

## **5️⃣ Validaciones en `argparse`**
📌 Se pueden forzar tipos de datos:
```python
parser.add_argument("-e", "--edad", type=int, required=True, help="Edad del usuario")
```
📌 Se pueden recibir listas:
```python
parser.add_argument("-n", "--numeros", type=int, nargs='+', help="Lista de números")
```
**Ejemplo de ejecución:**
```bash
python script.py -n 10 20 30
```
**Salida:**
```
[10, 20, 30]
```

---

## **6️⃣ Resumen Final**
✅ `sys.argv`: lista de argumentos sin validación.
✅ `getopt`: permite opciones `-n` y `--nombre`, pero es manual.
✅ `argparse`: la mejor opción, con validaciones y ayuda automática.

---

## **📖 Recursos adicionales**
🔗 [Documentación oficial de `argparse`](https://docs.python.org/3/library/argparse.html)
🔗 [Tutorial de `argparse` en Real Python](https://realpython.com/command-line-interfaces-python-argparse/)

🚀 ¡Listo para usar `argparse` en proyectos reales! 🎯
