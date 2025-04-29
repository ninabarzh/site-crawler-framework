"""
Generic crawler implementation for standard websites.
"""

import asyncio
from typing import Dict, Any
from pathlib import Path
from urllib.parse import urlparse

from src.core.base_crawler import BaseCrawler
from src.core import ContentHandler
from src.core import SiteType
from ..modules.url_utils import normalize_url, is_same_domain


class GenericCrawler(BaseCrawler):
    """Generic crawler for standard HTML websites."""

    def get_site_type(self) -> SiteType:
        return SiteType.GENERIC

    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """
        Crawl a URL and its links recursively.

        Args:
            url: URL to crawl
            depth: Current crawl depth

        Returns:
            Dictionary containing crawl results
        """
        if depth > self.config.get('max_depth', 3):
            return {}

        normalized_url = normalize_url(url)
        if not normalized_url or not self.is_allowed_url(normalized_url):
            return {}

        if normalized_url in self.visited_urls:
            return {}
        self.visited_urls.add(normalized_url)

        self.logger.info(f"Crawling {normalized_url} at depth {depth}")

        # Fetch the URL
        response = await self.fetch(normalized_url)
        if not response:
            return {}

        # Process content
        content_handler = ContentHandler(self.config)
        output_dir = Path(self.config['storage']['output_dir']) / urlparse(normalized_url).netloc
        result = content_handler.process_content(response, output_dir)

        # If HTML, extract links and crawl them
        if 'text/html' in response.get('content_type', ''):
            links = content_handler.extract_links(response['content'], normalized_url)

            # Crawl links asynchronously
            tasks = []
            for link in links:
                if is_same_domain(link, normalized_url):
                    tasks.append(self.crawl(link, depth + 1))

            if tasks:
                await asyncio.gather(*tasks)

        return result
