"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path
import tempfile


@pytest.fixture
def test_config():
    """Fixture providing a test configuration."""
    config = {
        'crawler': {
            'max_depth': 2,
            'request_timeout': 5,
            'concurrent_requests': 1,
            'politeness_delay': 0.1
        },
        'storage': {
            'output_dir': str(Path(tempfile.mkdtemp())),
            'save_html': True
        },
        'logging': {
            'level': 'DEBUG'
        }
    }
    return config


@pytest.fixture
def mock_sites_config():
    """Fixture providing mock sites configuration."""
    return {
        'sites': [
            {'url': 'http://example.com'},
            {'url': 'http://docs.example.org', 'type': 'sphinx'}
        ]
    }
