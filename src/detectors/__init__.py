"""
Package containing site detection functionality.
"""

from .detector import SiteDetector
from .strategies.flask_detector import FlaskDetector
from .strategies.sphinx_detector import SphinxDetector
from .strategies.wordpress_detector import WordPressDetector

__all__ = ['SiteDetector', 'FlaskDetector', 'SphinxDetector', 'WordPressDetector']
