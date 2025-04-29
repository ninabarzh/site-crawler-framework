"""
Abstract base class for all crawler implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from src.modules.request_handler import RequestHandler
from src.modules.url_utils import normalize_url
from src.modules.logger import get_logger
from src.modules.content_extractor import ContentExtractor
from src.core.exceptions import CrawlerError
from src.core.site_type import SiteType


class BaseCrawler(ABC):
    """Base class that all crawlers must inherit from."""

    def __init__(self, config: Dict[str, Any], site_config: Dict[str, Any]):
        """
        Initialize the crawler with global and site-specific configurations.

        Args:
            config: Global crawler configuration
            site_config: Site-specific configuration
        """
        self.config = config
        self.site_config = site_config
        self.logger = get_logger(self.__class__.__name__, config.get('logging', {}))
        self.request_handler = RequestHandler(config)
        self.content_extractor = ContentExtractor()
        self.visited_urls = set()

        # Validate and normalize the base URL
        self.base_url = self._validate_url(site_config['url'])
        self.allowed_domains = site_config.get('allowed_domains', [urlparse(self.base_url).netloc])

    @staticmethod
    def _validate_url(url: str) -> str:
        """Validate and normalize the URL."""
        normalized = normalize_url(url)
        if not normalized:
            raise CrawlerError(f"Invalid URL: {url}")
        return normalized

    def is_allowed_url(self, url: str) -> bool:
        """Check if a URL is allowed to be crawled based on domain restrictions."""
        parsed = urlparse(url)
        if not parsed.netloc:
            return False

        # Check against allowed domains
        return any(
            parsed.netloc == domain or parsed.netloc.endswith(f".{domain}")
            for domain in self.allowed_domains
        )

    @abstractmethod
    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """
        Main crawl method to be implemented by subclasses.

        Args:
            url: URL to crawl
            depth: Current crawl depth

        Returns:
            Dictionary containing crawl results
        """
        pass

    @abstractmethod
    def get_site_type(self) -> SiteType:
        """Return the site type this crawler is designed for."""
        pass

    async def fetch(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a URL with error handling and logging.

        Args:
            url: URL to fetch

        Returns:
            Dictionary containing response data or None if failed
        """
        try:
            response = await self.request_handler.get(url)
            if response and hasattr(response, 'status') and hasattr(response, 'content') and hasattr(response, 'headers'):
                return {
                    'url': url,
                    'status': response.status,
                    'content': response.content,
                    'content_type': response.headers.get('content-type'),
                    'headers': dict(response.headers)
                }
            return None
        except Exception as e:
            self.logger.warning(f"Failed to fetch {url}: {str(e)}")
            return None