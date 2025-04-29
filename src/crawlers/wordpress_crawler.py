"""
WordPress-specific crawler implementation.
"""

from typing import Dict, Any
from src.core.base_crawler import BaseCrawler
from src.core.site_type import SiteType


class WordPressCrawler(BaseCrawler):
    """Crawler specialized for WordPress sites."""

    def get_site_type(self) -> SiteType:
        return SiteType.WORDPRESS

    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """WordPress-specific crawling logic"""
        # Implement WordPress-specific crawling:
        # - Handle wp-json API
        # - Process posts/pages
        # - Handle pagination
        return await super().crawl(url, depth)
