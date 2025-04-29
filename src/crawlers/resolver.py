"""
Crawler class resolution based on site detection.
"""

from src.core.site_type import SiteType
from src.core.models import SiteConfig
from src.detectors import SiteDetector
from src.crawlers import (
    GenericCrawler,
    FlaskCrawler,
    SphinxCrawler,
    PDFCrawler,
    WordPressCrawler
)

class CrawlerResolver:
    def __init__(self, config: dict):
        self.detector = SiteDetector(config)
        self._init_detectors()

    def _init_detectors(self):
        """Initialize all detection strategies"""
        from src.detectors.strategies import (
            FlaskDetector,
            SphinxDetector,
            WordPressDetector,
            PDFDetector
        )
        self.detector.add_strategy(FlaskDetector())
        self.detector.add_strategy(SphinxDetector())
        self.detector.add_strategy(WordPressDetector())
        self.detector.add_strategy(PDFDetector())

    async def resolve(self, site_config: SiteConfig) -> type:
        """
        Resolve the appropriate crawler class using either:
        1. Explicit config type
        2. Automatic detection

        Args:
            site_config: Site configuration containing URL and optional type

        Returns:
            type: The appropriate crawler class for this site
        """
        # 1. Check for explicitly configured type
        if site_config.type:
            try:
                site_type = SiteType.from_string(site_config.type)
                return self._get_crawler_class(site_type)
            except ValueError:
                pass  # Fall through to detection

        # 2. Auto-detect site type
        site_type = await self.detector.detect(site_config.url)
        return self._get_crawler_class(site_type)

    @staticmethod
    def _get_crawler_class(site_type: SiteType) -> type:
        """
        Static method to map SiteType to crawler class.

        Args:
            site_type: The detected site type

        Returns:
            type: The crawler class to use (defaults to GenericCrawler)
        """
        return {
            SiteType.GENERIC: GenericCrawler,
            SiteType.FLASK: FlaskCrawler,
            SiteType.SPHINX: SphinxCrawler,
            SiteType.PDF: PDFCrawler,
            SiteType.WORDPRESS: WordPressCrawler
        }.get(site_type, GenericCrawler)
