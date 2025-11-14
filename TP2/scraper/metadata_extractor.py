from bs4 import BeautifulSoup

def extract_metadata(soup: BeautifulSoup) -> dict:
    """
    Extrae meta tags relevantes (description, keywords, Open Graph).
    """
    metas = {}
    
    # Description y keywords
    desc = soup.find('meta', attrs={'name': 'description'})
    if desc:
        metas['description'] = desc.get('content', '')
        
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    if keywords:
        metas['keywords'] = keywords.get('content', '')
        
    og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
    for tag in og_tags:
        metas[tag.get('property')] = tag.get('content', '')
        
    return metas