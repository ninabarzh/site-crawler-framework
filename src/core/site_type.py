"""
Site type definitions and utilities.
"""

from enum import Enum, auto
from typing import Type, TypeVar

T = TypeVar('T', bound='SiteType')

class SiteType(Enum):
    """Enumeration of supported site types."""
    GENERIC = auto()  # Standard HTML website
    FLASK = auto()    # Flask-powered web application
    SPHINX = auto()   # Sphinx documentation
    WORDPRESS = auto()  # WordPress site
    PDF = auto()      # PDF documents
    API = auto()      # REST API
    DYNAMIC = auto()  # JavaScript-heavy SPA

    @classmethod
    def from_string(cls: Type[T], type_str: str) -> T:
        """
        Convert string to SiteType enum.

        Args:
            type_str: String representation of the site type
                     (case-insensitive, e.g., "flask", "SPHINX")

        Returns:
            Corresponding SiteType enum member

        Example:
            >>> SiteType.from_string("flask")
            <SiteType.FLASK: 2>

            >>> SiteType.from_string("unknown")
            <SiteType.GENERIC: 1>
        """
        try:
            return cls[type_str.upper()]
        except KeyError:
            return cls.GENERIC