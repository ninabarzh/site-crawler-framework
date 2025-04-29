"""
Tests for Flask-specific crawler.
"""

import pytest
from unittest.mock import AsyncMock

from src.crawlers.flask_crawler import FlaskCrawler
from src.core.site_type import SiteType


@pytest.mark.asyncio
async def test_flask_crawler_type(test_config):
    """Test Flask crawler site type."""
    crawler = FlaskCrawler(test_config, {'url': 'http://flask.example.com'})
    assert crawler.get_site_type() == SiteType.FLASK


@pytest.mark.asyncio
async def test_flask_crawler_static(test_config):
    """Test Flask crawler static file handling."""
    crawler = FlaskCrawler(test_config, {'url': 'http://flask.example.com'})

    # Mock the parent crawl method
    crawler._BaseCrawler__crawl = AsyncMock(return_value={})

    await crawler.crawl('http://flask.example.com')

    # Should have tried to crawl static files
    crawler._BaseCrawler__crawl.assert_any_call('http://flask.example.com/static/', 1)
