"""
HTTP request handling with retries and rate limiting.
"""

import asyncio
import aiohttp
import logging
from typing import Optional, Dict, Any
from datetime import datetime


class RequestHandler:
    """Handles HTTP requests with retries and rate limiting."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the request handler.

        Args:
            config: Configuration dictionary
        """
        self.config = config.get('crawler', {})
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_request_time = 0
        self.session = None

    async def __aenter__(self):
        """Enter async context."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.get('request_timeout', 10)),
            headers={'User-Agent': self.config.get('user_agent', 'SiteCrawler/1.0')}
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Exit async context."""
        if self.session:
            await self.session.close()

    async def get(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET request with retries and rate limiting.

        Args:
            url: URL to request

        Returns:
            Dictionary containing response data or None if failed
        """
        if not self.session:
            raise RuntimeError("RequestHandler must be used as async context manager")

        # Respect politeness delay
        await self._wait_for_politeness()

        retries = self.config.get('retry_attempts', 3)
        for attempt in range(1, retries + 1):
            try:
                async with self.session.get(url) as response:
                    self.last_request_time = datetime.now().timestamp()

                    if response.status == 200:
                        return {
                            'url': str(response.url),
                            'status': response.status,
                            'content': await response.read(),
                            'headers': response.headers,
                            'content_type': response.headers.get('content-type')
                        }
                    else:
                        self.logger.warning(f"Request to {url} failed with status {response.status}")
                        return None

            except aiohttp.ClientError as e:
                self.logger.warning(f"Attempt {attempt}/{retries} failed for {url}: {str(e)}")
                if attempt == retries:
                    return None
                await asyncio.sleep(1)  # Wait before retry

        return None

    async def _wait_for_politeness(self):
        """Wait if needed to respect politeness delay."""
        delay = self.config.get('politeness_delay', 1.0)
        elapsed = datetime.now().timestamp() - self.last_request_time
        if elapsed < delay:
            await asyncio.sleep(delay - elapsed)
