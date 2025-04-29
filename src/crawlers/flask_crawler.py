"""
Specialized crawler for Flask-powered web applications.
"""

from typing import Dict, Any
from urllib.parse import urljoin

from src.core.base_crawler import BaseCrawler
from src.core import SiteType


class FlaskCrawler(BaseCrawler):
    """Crawler optimized for Flask web applications."""

    def get_site_type(self) -> SiteType:
        return SiteType.FLASK

    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """
        Crawl a Flask application with awareness of common patterns.
        """
        # First do everything the generic crawler would do
        result = await super().crawl(url, depth)

        # Flask-specific enhancements:
        # 1. Check for common Flask routes
        # 2. Look for Flask-specific patterns in templates
        # 3. Handle dynamic content generation

        # Example: Check for common Flask static files
        static_url = urljoin(url, '/static/')
        if depth == 0:  # Only crawl static at top level
            await super().crawl(static_url, depth + 1)

        return result
