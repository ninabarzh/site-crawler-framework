"""
Data models for configuration using Pydantic.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class CrawlerConfig(BaseModel):
    timeout: int = 30  # Default timeout in seconds
    max_retries: int = 3
    user_agent: str
    logging: Dict[str, Any]

class SiteConfig(BaseModel):
    url: str
    type: Optional[str] = None
    allowed_domains: Optional[List[str]] = None
