import aiohttp
import asyncio

async def fetch_page(session: aiohttp.ClientSession, url: str) -> (str, str): # type: ignore
    """
    Descarga el contenido HTML de una URL de forma asíncrona.
    """
    # Timeout
    timeout = aiohttp.ClientTimeout(total=30.0)
    
    print(f"Scraper: Iniciando descarga de {url}")
    try:
        async with session.get(url, timeout=timeout, allow_redirects=True) as response:
            # Lanza excepción si el status es 4xx o 5xx
            response.raise_for_status() 
            
            if 'text/html' not in response.content_type:
                raise ValueError(f"El contenido no es HTML ({response.content_type})")
            
            html = await response.text()
            
            return html, str(response.url)
            
    except asyncio.TimeoutError:
        print(f"Error: Timeout de 30s excedido para {url}")
        raise
    except aiohttp.ClientError as e:
        print(f"Error de cliente HTTP para {url}: {e}")
        raise