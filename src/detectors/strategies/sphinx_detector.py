"""
Detection strategy for Sphinx documentation sites.

Identifies Sphinx sites by checking for:
- Characteristic CSS classes and IDs
- Standard documentation structure
- Common static file paths
- Sphinx-specific HTML patterns
"""

import re
from typing import Dict, Any
from src.core.site_type import SiteType


class SphinxDetector:
    """Detects Sphinx documentation sites."""

    site_type = SiteType.SPHINX

    @staticmethod
    async def detect(response: Dict[str, Any]) -> bool:
        """
        Detect if a site is Sphinx documentation.

        Args:
            response: Dictionary containing response data

        Returns:
            bool: True if Sphinx is detected with high confidence
        """
        if 'text/html' not in response.get('content_type', ''):
            return False

        try:
            html = response['content'].decode('utf-8', errors='ignore')
            return any([
                re.search(r'class="[^"]*(?:document|sphinx|body)', html),
                re.search(r'<div[^>]*id="(?:searchbox|sidebar|related)"', html),
                re.search(r'/_static/|/_sources/|/_images/', html)
            ])
        except (KeyError, UnicodeError) as error:
            print(f"Sphinx detection error: {error}")
            return False
