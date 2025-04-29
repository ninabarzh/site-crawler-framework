"""
Crawlers package initialization.
"""

from .generic_crawler import GenericCrawler
from .flask_crawler import FlaskCrawler
from .sphinx_crawler import SphinxCrawler
from .pdf_crawler import PDFCrawler
from .wordpress_crawler import WordPressCrawler
from .resolver import CrawlerResolver
from .manager import CrawlerManager

__all__ = [
    'GenericCrawler',
    'FlaskCrawler',
    'SphinxCrawler',
    'PDFCrawler',
    'WordPressCrawler',
    'CrawlerResolver',
    'CrawlerManager'
]