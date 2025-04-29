"""
URL manipulation and validation utilities.
"""

from urllib.parse import urlparse
from typing import Optional

def normalize_url(url: str) -> Optional[str]:
    """
    Normalize a URL by:
    - Ensuring it has a scheme
    - Removing fragments
    - Removing query parameters (optional)
    - Lowercasing the hostname

    Args:
        url: URL to normalize

    Returns:
        Normalized URL or None if invalid
    """
    if not url or not isinstance(url, str):
        return None

    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return None

        # Reconstruct URL with normalized components
        normalized = parsed._replace(
            scheme='https' if parsed.scheme == 'http' and parsed.port == 443 else parsed.scheme,
            netloc=parsed.netloc.lower(),
            path=parsed.path.rstrip('/') or '/',
            query='',
            fragment=''
        )
        return normalized.geturl()
    except ValueError:
        return None

def is_same_domain(url1: str, url2: str) -> bool:
    """
    Check if two URLs belong to the same domain.

    Args:
        url1: First URL
        url2: Second URL

    Returns:
        True if same domain, False otherwise
    """
    domain1 = get_domain(url1)
    domain2 = get_domain(url2)
    return domain1 and domain2 and domain1 == domain2

def get_domain(url: str) -> Optional[str]:
    """
    Extract the registered domain from a URL.

    Args:
        url: URL to extract domain from

    Returns:
        Registered domain or None if invalid URL
    """
    parsed = urlparse(normalize_url(url) or '')
    if not parsed.netloc:
        return None

    # Simple implementation - for production use tldextract
    parts = parsed.netloc.split('.')
    if len(parts) >= 2:
        return '.'.join(parts[-2:])
    return parsed.netloc
