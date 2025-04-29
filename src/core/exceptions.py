"""
Custom exceptions for the crawler framework.
"""

class CrawlerError(Exception):
    """Base exception for all crawler-related errors."""
    pass

class ConfigError(CrawlerError):
    """Exception for configuration-related errors."""
    pass

class DetectionError(CrawlerError):
    """Exception for site detection failures."""
    pass

class RequestError(CrawlerError):
    """Exception for HTTP request failures."""
    pass

class StorageError(CrawlerError):
    """Exception for content storage failures."""
    pass
