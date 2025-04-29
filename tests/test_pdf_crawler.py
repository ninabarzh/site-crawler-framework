"""
Tests for PDF crawler.
"""

import pytest
from unittest.mock import AsyncMock

from src.crawlers.pdf_crawler import PDFCrawler
from src.core.site_type import SiteType


@pytest.mark.asyncio
async def test_pdf_crawler_type(test_config):
    """Test PDF crawler site type."""
    crawler = PDFCrawler(test_config, {'url': 'http://example.com/doc.pdf'})
    assert crawler.get_site_type() == SiteType.PDF


@pytest.mark.asyncio
async def test_pdf_crawler_skip_non_pdf(test_config):
    """Test PDF crawler skips non-PDF URLs."""
    crawler = PDFCrawler(test_config, {'url': 'http://example.com/doc.pdf'})

    # Mock fetch to return non-PDF content
    crawler.fetch = AsyncMock(return_value={
        'content': b'not a pdf',
        'content_type': 'text/html',
        'status': 200
    })

    result = await crawler.crawl('http://example.com/doc.pdf')
    assert result == {}
