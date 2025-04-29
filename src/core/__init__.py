"""
Core module containing the fundamental components of the web crawler framework.
"""

from .base_crawler import BaseCrawler
from .content_handler import ContentHandler
from .exceptions import CrawlerError, ConfigError, DetectionError
from .site_type import SiteType

__all__ = ['BaseCrawler', 'ContentHandler', 'CrawlerError', 'ConfigError', 'DetectionError', 'SiteType']