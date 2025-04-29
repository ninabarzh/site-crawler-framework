"""
File handling and storage utilities.
"""

import hashlib
import logging
from pathlib import Path
from urllib.parse import urlparse


def safe_filename(url: str) -> str:
    """
    Create a safe filename from a URL.

    Args:
        url: URL to convert to filename

    Returns:
        Safe filename string
    """
    # Use hash of URL as base filename
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    parsed = urlparse(url)

    # Get the last part of the path
    path_part = parsed.path.split('/')[-1] if parsed.path else 'index'

    # Combine with hash to avoid collisions
    return f"{path_part[:50]}_{url_hash[:8]}"


class FileHandler:
    """Handles file storage operations."""

    def __init__(self, config: dict):
        """
        Initialize the file handler.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def save_html(self, content: bytes, url: str, output_dir: Path) -> Path:
        """
        Save HTML content to a file.

        Args:
            content: HTML content as bytes
            url: Source URL
            output_dir: Directory to save file

        Returns:
            Path to saved file

        Raises:
            IOError: If file cannot be saved
        """
        filename = safe_filename(url) + '.html'
        filepath = output_dir / filename

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save HTML from {url}: {str(e)}")
            raise

    def save_pdf(self, content: bytes, url: str, output_dir: Path) -> Path:
        """
        Save PDF content to a file.

        Args:
            content: PDF content as bytes
            url: Source URL
            output_dir: Directory to save file

        Returns:
            Path to saved file

        Raises:
            IOError: If file cannot be saved
        """
        filename = safe_filename(url) + '.pdf'
        filepath = output_dir / 'pdfs' / filename

        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save PDF from {url}: {str(e)}")
            raise
