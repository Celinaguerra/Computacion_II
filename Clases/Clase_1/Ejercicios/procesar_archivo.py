import argparse

def main():
    parser = argparse.ArgumentParser(description="Ejemplo de procesar archivo")
    parser.add_argument("-i", "--input", required=True, help="Archivo de entrada")
    parser.add_argument("-o", "--output", required=True, help="Archivo de salida")

    args = parser.parse_args()


    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

if __name__ == "__main__":
    main()