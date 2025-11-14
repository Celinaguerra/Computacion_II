from playwright.sync_api import Page
import base64

def generate_screenshot(page: Page) -> str:
    """
    Toma una captura de pantalla de la página ya cargada.
    Devuelve la imagen PNG como un string base64.
    """
    print("Worker: Generando screenshot...")
    try:
        # ss de la página completa
        png_bytes = page.screenshot(
            full_page=True,
            timeout=10000
        )
        return base64.b64encode(png_bytes).decode('utf-8')
    
    except Exception as e:
        print(f"Worker Error: Falló al tomar screenshot: {e}")
        return f"Error al generar screenshot: {e}"