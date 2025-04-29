"""
Package containing individual detection strategies.
"""

from .flask_detector import FlaskDetector
from .sphinx_detector import SphinxDetector
from .wordpress_detector import WordPressDetector
from .pdf_detector import PDFDetector

__all__ = [
    'FlaskDetector',
    'SphinxDetector',
    'WordPressDetector',
    'PDFDetector'
]
