"""
Content handling and processing functionality.
"""

from typing import Dict, Any, List
import logging
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from ..modules.file_handler import FileHandler


class ContentHandler:
    """Handles content processing and storage."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the content handler.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.file_handler = FileHandler(config)
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def extract_links(html: str, base_url: str) -> List[str]:
        """
        Extract all links from HTML content.

        Args:
            html: HTML content as string
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href'].strip()
            if not href or href.startswith('#'):
                continue

            # Handle relative URLs
            if href.startswith('/'):
                href = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}{href}"
            elif not href.startswith(('http://', 'https://')):
                href = f"{base_url}/{href}" if not base_url.endswith('/') else f"{base_url}{href}"

            links.append(href)

        return links

    def process_content(self, response: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
        """
        Process and save content based on its type.

        Args:
            response: Dictionary containing response data
            output_dir: Directory to save content

        Returns:
            Dictionary with processing results
        """
        result = {
            'url': response['url'],
            'status': response['status'],
            'content_type': response['content_type'],
            'saved_path': None,
            'metadata': {}
        }

        content_type = response['content_type'] or ''

        try:
            if 'text/html' in content_type:
                if self.config.get('storage', {}).get('save_html', True):
                    filename = self.file_handler.save_html(
                        response['content'],
                        response['url'],
                        output_dir
                    )
                    result['saved_path'] = str(filename)

                # Extract metadata from HTML
                soup = BeautifulSoup(response['content'], 'html.parser')
                result['metadata']['title'] = soup.title.string if soup.title else None

            elif 'application/pdf' in content_type:
                if self.config.get('storage', {}).get('save_pdf', True):
                    filename = self.file_handler.save_pdf(
                        response['content'],
                        response['url'],
                        output_dir
                    )
                    result['saved_path'] = str(filename)

            # Add more content type handlers as needed

        except Exception as e:
            self.logger.error(f"Error processing content from {response['url']}: {str(e)}")

        return result
