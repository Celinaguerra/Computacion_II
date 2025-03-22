import sys
import getopt

def main():
    # Definir opciones cortas (-n) y largas (--nombre)
    opciones_cortas = "n:e:"  # `:` indica que requieren valor
    opciones_largas = ["nombre=", "edad="]

    try:
        opts, args = getopt.getopt(sys.argv[1:], opciones_cortas, opciones_largas)
    except getopt.GetoptError as err:
        print("Error:", err)
        sys.exit(1)

    # Procesar opciones
    nombre = None
    edad = None
    for opt, val in opts:
        if opt in ("-n", "--nombre"):
            nombre = val
        elif opt in ("-e", "--edad"):
            edad = val

    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")

if __name__ == "__main__":
    main()
