"""
Utility modules for the crawler framework.

Provides:
- Configuration loading (YAML/JSON)
- Content extraction via ContentExtractor class
- File handling operations
- Logging utilities
- Network request handling
- URL manipulation tools
"""

from .config_loader import load_config, validate_config
from .content_extractor import ContentExtractor
from .file_handler import FileHandler
from .logger import get_logger, setup_logging
from .request_handler import RequestHandler
from .url_utils import normalize_url, is_same_domain, get_domain

# Create direct function aliases
extract_pdf = ContentExtractor.extract_text_from_pdf
extract_html = ContentExtractor.extract_text_from_html
extract_docx = ContentExtractor.extract_text_from_docx
extract_pptx = ContentExtractor.extract_text_from_pptx

__all__ = [
    # Configuration
    'load_config',
    'validate_config',

    # Content Extraction
    'ContentExtractor',
    'extract_pdf',
    'extract_html',
    'extract_docx',
    'extract_pptx',
    'PDFSyntaxError',

    # File Operations
    'FileHandler',

    # Logging
    'get_logger',
    'setup_logging',

    # Networking
    'RequestHandler',

    # URL Utilities
    'normalize_url',
    'is_same_domain',
    'get_domain'
]

__version__ = "1.2.0"