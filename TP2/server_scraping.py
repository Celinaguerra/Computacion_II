import asyncio
import aiohttp
from aiohttp import web
import argparse
import sys
import ipaddress
import json
from datetime import datetime, timezone
from bs4 import BeautifulSoup

from common.protocol import async_send_msg, async_recv_msg
from scraper.async_http import fetch_page
from scraper.html_parser import parse_html_structure
from scraper.metadata_extractor import extract_metadata

SERVER_B_HOST = '127.0.0.1'
SERVER_B_PORT = 9001

async def contact_server_b(payload: dict) -> dict:
    """
    Se conecta al Servidor B, envía la solicitud
    y espera la respuesta.
    """
    print("Servidor A: Contactando al Servidor B...")
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(SERVER_B_HOST, SERVER_B_PORT),
            timeout=5.0
        )
    except (asyncio.TimeoutError, ConnectionRefusedError) as e:
        print(f"Servidor A: Error al conectar con Servidor B: {e}")
        return {"status": "error", "message": f"No se pudo conectar al Servidor B: {e}"}

    try:
        await async_send_msg(writer, payload)
        response = await asyncio.wait_for(async_recv_msg(reader), timeout=60.0)
        
        print("Servidor A: Respuesta recibida del Servidor B.")
        return response
        
    except (asyncio.TimeoutError, ConnectionError) as e:
        print(f"Servidor A: Error de comunicación con Servidor B: {e}")
        return {"status": "error", "message": f"Error de comunicación con Servidor B: {e}"}
    finally:
        writer.close()
        await writer.wait_closed()


async def handle_scrape(request: web.Request) -> web.Response:
    """
    Handler principal de aiohttp para la ruta /scrape
    """
    url = request.query.get('url')
    if not url:
        return web.json_response(
            {"status": "error", "message": "Parámetro 'url' requerido"},
            status=400
        )
    
    print(f"\nServidor A: Petición recibida para: {url}")
    
    session = request.app['http_session']
    final_json = {"url": url}

    try:
        html_content, real_url = await fetch_page(session, url)
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        scraping_data = parse_html_structure(soup)
        meta_tags = extract_metadata(soup)
        
        image_urls = scraping_data.pop("_image_urls_for_b")
        payload_for_b = {
            "url": real_url,
            "image_urls": image_urls
        }
        
        processing_results = await contact_server_b(payload_for_b)
        
        # Formato de respuesta
        final_json.update({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scraping_data": {
                **scraping_data,
                "meta_tags": meta_tags,
            },
            "processing_data": {
                "screenshot": processing_results.get("browser_data", {}).get("screenshot", "Error"),
                "performance": processing_results.get("browser_data", {}).get("performance", "Error"),
                "thumbnails": processing_results.get("image_data", {}).get("thumbnails", "Error")
            },
            "status": "success"
        })
        
        return web.json_response(final_json)

    except (aiohttp.ClientError, ValueError, asyncio.TimeoutError) as e:
        print(f"Servidor A: Error procesando {url}: {e}")
        final_json.update({
            "status": "error",
            "message": f"Error al procesar la URL: {e}"
        })
        return web.json_response(final_json, status=500)


async def setup_http_session(app: web.Application):
    """Inicializa la sesión de aiohttp."""
    print("Servidor A: Creando ClientSession de aiohttp...")
    app['http_session'] = aiohttp.ClientSession()

async def cleanup_http_session(app: web.Application):
    """Cierra la sesión de aiohttp."""
    print("\nServidor A: Cerrando ClientSession...")
    await app['http_session'].close()

def main():
    parser = argparse.ArgumentParser(
        description="Servidor de Scraping Web Asíncrono (Parte A)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--ip', required=True,
        help="Dirección de escucha (soporta IPv4/IPv6, ej: 0.0.0.0 o ::)"
    )
    parser.add_argument(
        '-p', '--port', required=True, type=int,
        help="Puerto de escucha"
    )
    parser.add_argument(
        '-w', '--workers', type=int, default=4,
        help="Número de workers (default: 4) - (Nota: aiohttp usa un worker por defecto)"
    )
    args = parser.parse_args()

    # Validar IP
    try:
        ipaddress.ip_address(args.ip)
    except ValueError:
        print(f"Error: Dirección IP inválida: {args.ip}", file=sys.stderr)
        sys.exit(1)

    app = web.Application()
    app.router.add_get('/scrape', handle_scrape)
    
    app.on_startup.append(setup_http_session)
    app.on_cleanup.append(cleanup_http_session)

    print(f"--- Servidor A (Scraping) ---")
    print(f"Asegúrate de que el Servidor B esté corriendo en {SERVER_B_HOST}:{SERVER_B_PORT}")
    
    try:
        web.run_app(
            app,
            host=args.ip,
            port=args.port
        )
    except KeyboardInterrupt:
        print("\nServidor A detenido.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: El puerto {args.port} en {args.ip} ya está en uso.", file=sys.stderr)
        else:
            print(f"Error de OS: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()