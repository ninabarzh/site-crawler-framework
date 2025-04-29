"""
Detection strategy for Flask applications.

Identifies Flask web applications by checking for:
- Flask-specific error page patterns
- Jinja2 template syntax (both {{ }} and {% %} styles)
- Common static file paths
- Default Flask headers
"""

import re
from typing import Dict, Any
from src.core.site_type import SiteType


class FlaskDetector:
    """Detects Flask web applications."""

    site_type = SiteType.FLASK

    @staticmethod
    async def detect(response: Dict[str, Any]) -> bool:
        """
        Detect if a site is built with Flask.

        Args:
            response: Dictionary containing:
                     - content: Raw HTML bytes
                     - content_type: Response content type
                     - headers: Response headers

        Returns:
            bool: True if Flask is detected with high confidence
        """
        if 'text/html' not in response.get('content_type', ''):
            return False

        try:
            html = response['content'].decode('utf-8', errors='ignore')

            # Check multiple Flask indicators
            return any([
                # Flask framework patterns
                re.search(r'flask\.(?:app|debughelpers)', html, re.I),

                # Jinja2 template patterns (simplified)
                re.search(r'{{.*?}}|{%-? .*? -?%}', html),

                # Static file path pattern
                '/static/' in html,

                # Header-based detection
                'flask' in (response.get('headers', {}).get('x-powered-by', '').lower())
            ])
        except (KeyError, UnicodeError) as error:
            print(f"Flask detection error: {error}")
            return False