"""
Detection strategy for WordPress sites.

Identifies WordPress by checking for:
- Characteristic meta tags
- Standard WordPress paths
- Admin bar presence
- WP-specific HTTP headers
"""

import re
from typing import Dict, Any
from src.core.site_type import SiteType


class WordPressDetector:
    """Detects WordPress sites."""

    site_type = SiteType.WORDPRESS

    @staticmethod
    async def detect(response: Dict[str, Any]) -> bool:
        """
        Detect if a site is built with WordPress.

        Args:
            response: Dictionary containing response data

        Returns:
            bool: True if WordPress is detected with high confidence
        """
        headers = response.get('headers', {})

        # Check headers first (faster)
        if any([
            'wordpress' in headers.get('x-powered-by', '').lower(),
            'wp-json' in headers.get('link', '')
        ]):
            return True

        if 'text/html' not in response.get('content_type', ''):
            return False

        try:
            html = response['content'].decode('utf-8', errors='ignore')
            return any([
                re.search(r'<meta[^>]+name="generator"[^>]+content="wordpress', html, re.I),
                re.search(r'/wp-content/|/wp-includes/', html),
                'wpadminbar' in html
            ])
        except (KeyError, UnicodeError) as error:
            print(f"WordPress detection error: {error}")
            return False
