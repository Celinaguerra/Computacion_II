import requests
import base64
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin

def process_thumbnails(base_url: str, image_urls: list) -> list:
    """
    Descarga las imágenes principales (máximo 5),
    genera thumbnails 128x128 y los devuelve como
    lista de strings base64 (PNG).
    """
    print(f"Worker: Procesando {len(image_urls)} thumbnails...")
    thumbnails_b64 = []
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...'
    })
    
    # Procesamos un máximo de 5 imágenes
    for img_url in image_urls[:5]:
        try:
            full_url = urljoin(base_url, img_url)
            
            response = session.get(full_url, timeout=5)
            response.raise_for_status()
            
            img_data = BytesIO(response.content)
            with Image.open(img_data) as img:
                img.thumbnail((128, 128))
                
                output_buffer = BytesIO()
                img.save(output_buffer, format="PNG")
                
                # Convertir a base64
                img_bytes = output_buffer.getvalue()
                b64_str = base64.b64encode(img_bytes).decode('utf-8')
                thumbnails_b64.append(b64_str)
                
        except Exception as e:
            print(f"Worker Warning: No se pudo procesar imagen {img_url}: {e}")

    print(f"Worker: Thumbnails generados: {len(thumbnails_b64)}")
    return thumbnails_b64