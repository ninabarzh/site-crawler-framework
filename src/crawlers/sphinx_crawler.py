"""
Specialized crawler for Sphinx documentation sites.
"""

from typing import Dict, Any
from urllib.parse import urljoin

from src.core.base_crawler import BaseCrawler
from src.core import SiteType


class SphinxCrawler(BaseCrawler):
    """Crawler optimized for Sphinx documentation sites."""

    def get_site_type(self) -> SiteType:
        return SiteType.SPHINX

    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """
        Crawl a Sphinx documentation site with awareness of its structure.
        """
        result = await super().crawl(url, depth)

        # Sphinx-specific enhancements:
        # 1. Check for _static and _sources directories
        # 2. Look for search.html and genindex.html
        # 3. Handle PDF documentation if configured

        if self.site_config.get('include_pdf', False):
            pdf_url = urljoin(url, '/_downloads/')
            await super().crawl(pdf_url, depth + 1)

        return result
