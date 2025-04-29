"""
Tests for site detection functionality.
"""

import pytest
from unittest.mock import AsyncMock

from src.detectors.detector import SiteDetector
from src.detectors.strategies.flask_detector import FlaskDetector
from src.detectors.strategies.sphinx_detector import SphinxDetector
from src.core.site_type import SiteType


@pytest.mark.asyncio
async def test_flask_detection(test_config):
    """Test Flask site detection."""
    detector = SiteDetector(test_config)
    detector.add_strategy(FlaskDetector())

    # Mock the request handler to return our test response
    mock_response = {
        'content': b'<html><body><div class="flask-app">Test</div></body></html>',
        'content_type': 'text/html',
        'headers': {}
    }
    detector.request_handler.get = AsyncMock(return_value=mock_response)

    # Should detect Flask
    assert await detector.detect('http://flask.example.com') == SiteType.FLASK


@pytest.mark.asyncio
async def test_sphinx_detection(test_config):
    """Test Sphinx site detection."""
    detector = SiteDetector(test_config)
    detector.add_strategy(SphinxDetector())

    # Mock the request handler to return our test response
    mock_response = {
        'content': b'<html><body><div class="sphinxsidebar">Test</div></body></html>',
        'content_type': 'text/html',
        'headers': {}
    }
    detector.request_handler.get = AsyncMock(return_value=mock_response)

    # Should detect Sphinx
    assert await detector.detect('http://docs.example.org') == SiteType.SPHINX