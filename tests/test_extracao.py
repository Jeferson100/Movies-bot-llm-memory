from unittest.mock import patch
from extracao import (LinksExtractor,
                    LinksExtractorHtml2Text,
)
import asyncio

def test_extracao_textos_links_crawl4ai():
    with patch('extracao.extracao_textos_links_crawl4ai', return_value="extracao_crawl4ai"):
        url = "https://www.crawl4ai.com/"
        extracao = LinksExtractor()
        result = asyncio.run(extracao.extract_links(url))
        assert result is not None
        
def test_extracao_textos_links_html2text():
    with patch('extracao.extracao_textos_links_html2text', return_value="extracao_html2text"):
        url = "https://www.crawl4ai.com/"
        extracao = LinksExtractorHtml2Text()
        result = extracao.extrair_links_html2text(url)
        assert result is not None
        
def test_extracao_textos_clean_crawl4ai():
    with patch('extracao.extracao_textos_links_crawl4ai', return_value="extracao_clean_crawl4ai"):
        url = "https://www.crawl4ai.com/"
        extracao = LinksExtractor()
        result = extracao.clean_text(url)
        assert result is not None
        assert 'https' not in result
        assert '[' not in result
        
def test_extracao_textos_clean_html2text():
    with patch('extracao.extracao_textos_links_html2text', return_value="extracao_clean_html2text"):
        url = "https://www.crawl4ai.com/"
        extracao = LinksExtractorHtml2Text()
        result = extracao.clean_text_html2text(url)
        assert result is not None
        assert 'https' not in result
        assert '[' not in result
        assert len(result.strip()) > 10
        
        
        