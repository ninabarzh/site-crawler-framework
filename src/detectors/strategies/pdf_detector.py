"""
Detection strategy for PDF documents.
"""

import re
from typing import Dict, Any
from src.core.site_type import SiteType

class PDFDetector:
    """Detects PDF documents using content type and URL patterns."""

    site_type = SiteType.PDF

    @staticmethod
    async def detect(response: Dict[str, Any]) -> bool:
        """
        Detect if response is a PDF document.

        Args:
            response: Dictionary containing:
                     - content: Raw bytes of response
                     - content_type: Response content type
                     - url: Request URL

        Returns:
            bool: True if PDF is detected
        """
        content_type = response.get('content_type', '')
        url = response.get('url', '')

        # Primary check for PDF content type
        if 'application/pdf' in content_type:
            return True

        # Secondary check for PDF links in HTML
        if 'text/html' in content_type:
            content = response.get('content')
            if content and isinstance(content, bytes):
                try:
                    html = content.decode('utf-8', errors='ignore')
                    return bool(re.search(r'\.pdf([\'"]|$)', html, re.I))
                except UnicodeError:
                    pass

        # Tertiary check for PDF in URL
        return bool(re.search(r'\.pdf$', url, re.I))
