from bs4 import BeautifulSoup 

def parse_html_structure(soup: BeautifulSoup) -> dict:
    """
    Parsea el HTML y extrae la estructura solicitada.
    """
    
    title = soup.title.string.strip() if soup.title else 'N/A'
    
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    
    image_tags = soup.find_all('img', src=True)
    images_count = len(image_tags)
    image_urls = [img.get('src') for img in image_tags[:10]]
    
    structure = {}
    for i in range(1, 7):
        tag = f'h{i}'
        structure[tag] = len(soup.find_all(tag))
        
    return {
        "title": title,
        "links": links,
        "images_count": images_count,
        "structure": structure,
        "_image_urls_for_b": image_urls
    }