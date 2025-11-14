import pytest
from bs4 import BeautifulSoup

from scraper.html_parser import parse_html_structure
from scraper.metadata_extractor import extract_metadata

MOCK_HTML = """
<html>
  <head>
    <title>Título de Prueba </title>
    <meta name="description" content="Mi descripción">
    <meta property="og:title" content="Título OG">
  </head>
  <body>
    <h1>Un header</h1>
    <h1>Otro header</h1>
    <a href="/link1">Link 1</a>
    <img src="img1.png">
  </body>
</html>
"""

@pytest.fixture
def soup():
    return BeautifulSoup(MOCK_HTML, 'lxml')

def test_parse_html_structure(soup):
    structure = parse_html_structure(soup)
    
    assert structure['title'] == 'Título de Prueba'
    assert structure['links'] == ['/link1']
    assert structure['images_count'] == 1
    assert structure['structure']['h1'] == 2
    assert structure['structure']['h2'] == 0
    assert structure['_image_urls_for_b'] == ['img1.png']

def test_extract_meta_tags(soup):
    """
    Este test ya estaba bien, usaba 'soup' correctamente.
    """
    metas = extract_metadata(soup)
    
    assert metas['description'] == 'Mi descripción'
    assert metas['og:title'] == 'Título OG'
    assert 'keywords' not in metas