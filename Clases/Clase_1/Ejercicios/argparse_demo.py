import argparse

def main():
    parser = argparse.ArgumentParser(description="Ejemplo de argparse")
    parser.add_argument("-n", "--nombre", required=True, help="Nombre del usuario")
    parser.add_argument("-e", "--edad", type=int, help="Edad del usuario")
    
    args = parser.parse_args()
    
    print(f"Nombre: {args.nombre}")
    if args.edad:
        print(f"Edad: {args.edad}")

if __name__ == "__main__":
    main()
