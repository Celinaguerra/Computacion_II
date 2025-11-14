import socketserver
import argparse
import sys
import ipaddress
import socket
from multiprocessing import Pool, cpu_count
import functools  

from common.protocol import sync_send_msg, sync_recv_msg

from processor.screenshot import generate_screenshot
from processor.performance import analyze_performance
from processor.image_processor import process_thumbnails

def run_browser_tasks(url: str) -> dict:
    """
    Worker: Ejecuta todas las tareas de Playwright (Screenshot y Perf.)
    """
    print(f"Worker (PID {sys.argv[0]}): Iniciando tareas de browser para {url}")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=20000)
            
            screenshot_b64 = generate_screenshot(page)
            performance_data = analyze_performance(page)
            
            browser.close()
            
            return {
                "status": "success",
                "screenshot": screenshot_b64,
                "performance": performance_data
            }
        except Exception as e:
            if browser:
                browser.close()
            print(f"Worker Error: Fallaron tareas de browser para {url}: {e}")
            return {"status": "error", "error": str(e)}

def run_image_tasks(base_url: str, image_urls: list) -> dict:
    """
    Worker: Ejecuta la tarea de procesamiento de imágenes.
    """
    print(f"Worker (PID {sys.argv[0]}): Iniciando tareas de imágenes para {base_url}")
    try:
        thumbnails = process_thumbnails(base_url, image_urls)
        return {"status": "success", "thumbnails": thumbnails}
    except Exception as e:
        print(f"Worker Error: Fallaron tareas de imágenes: {e}")
        return {"status": "error", "error": str(e)}


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Servidor TCP que usa Threads para manejar cada conexión.
    """
    daemon_threads = True
    allow_reuse_address = True
    process_pool: Pool = None  # type: ignore

class ProcessingHandler(socketserver.BaseRequestHandler):
    """
    Handler para cada conexión del Servidor A.
    Este handler se ejecuta en su propio THREAD.
    """
    def handle(self):
        print(f"Servidor B: Conexión recibida de {self.client_address}")
        
        try:
            data = sync_recv_msg(self.request)
            if data.get("error"):
                raise ValueError(data["error"])

            url = data.get("url")
            image_urls = data.get("image_urls")
            
            if not url:
                raise ValueError("No se recibió URL en la solicitud")

            pool = self.server.process_pool
            
            async_result_browser = pool.apply_async(run_browser_tasks, (url,))
            async_result_images = pool.apply_async(run_image_tasks, (url, image_urls))
            
            browser_results = async_result_browser.get(timeout=60)
            image_results = async_result_images.get(timeout=60)
            
            final_response = {
                "browser_data": browser_results,
                "image_data": image_results
            }
            sync_send_msg(self.request, final_response)
            
        except Exception as e:
            print(f"Servidor B: Error al manejar {self.client_address}: {e}")
            try:
                sync_send_msg(self.request, {"status": "error", "message": str(e)})
            except Exception:
                pass 
        
        print(f"Servidor B: Conexión con {self.client_address} cerrada.")

def main():
    parser = argparse.ArgumentParser(
        description="Servidor de Procesamiento Distribuido (Parte B)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--ip', required=True,
        help="Dirección de escucha (IPv4 o IPv6)"
    )
    parser.add_argument(
        '-p', '--port', required=True, type=int,
        help="Puerto de escucha"
    )
    parser.add_argument(
        '-n', '--processes', type=int, default=None,
        help="Número de procesos en el pool (default: CPU count)"
    )
    args = parser.parse_args()

    try:
        ip_addr = ipaddress.ip_address(args.ip)
        if ip_addr.version == 4:
            address_family = socket.AF_INET
        else:
            address_family = socket.AF_INET6
    except ValueError:
        print(f"Error: Dirección IP inválida: {args.ip}", file=sys.stderr)
        sys.exit(1)


    num_processes = args.processes if args.processes else cpu_count()
    
    with Pool(processes=num_processes, maxtasksperchild=5) as pool:
        
        ThreadedTCPServer.address_family = address_family
        server = ThreadedTCPServer((args.ip, args.port), ProcessingHandler)
        server.process_pool = pool
        
        host, port = server.server_address[:2]
        print(f"--- Servidor B (Procesamiento) ---")
        # <-- MODIFICADO: Mensaje actualizado -->
        print(f"Usando {num_processes} procesos worker (multiprocessing.Pool).")
        print(f"Escuchando en {host} (IPv{ip_addr.version}) puerto {port}...")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor B detenido.")
            server.shutdown()

if __name__ == "__main__":
    main()