"""
Main site detection logic that uses strategy pattern.

Implements the core detection framework that:
- Manages multiple detection strategies
- Coordinates detection attempts
- Provides fallback to GENERIC site type
"""

from typing import Dict, Any
from src.core.site_type import SiteType
from src.core.exceptions import DetectionError
from src.modules.request_handler import RequestHandler


class SiteDetector:
    """Detects the type of website using multiple strategies."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the detector with configuration.

        Args:
            config: Crawler configuration dictionary containing:
                   - request_handler: Configuration for HTTP requests
                   - detection: Strategy-specific settings
        """
        self.config = config
        self.request_handler = RequestHandler(config)
        self.strategies = []

    def add_strategy(self, strategy):
        """Add a detection strategy to the detection pipeline."""
        self.strategies.append(strategy)

    async def detect(self, url: str) -> SiteType:
        """
        Detect the site type by trying all available strategies.

        Args:
            url: URL to detect

        Returns:
            Detected SiteType (falls back to GENERIC if no match)

        Raises:
            DetectionError: If no strategies configured or failed to fetch URL
        """
        if not self.strategies:
            raise DetectionError("No detection strategies configured")

        response = await self.request_handler.get(url)
        if not response:
            raise DetectionError(f"Failed to fetch URL for detection: {url}")

        for strategy in self.strategies:
            try:
                if await strategy.detect(response):
                    return strategy.site_type
            except Exception as e:
                self.config.get('logger', print)(f"Detection strategy failed: {str(e)}")
                continue

        return SiteType.GENERIC
