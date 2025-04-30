# Extending the Framework

## Creating a new crawler

1. Create `crawlers/my_crawler.py`:

```python
from src.core.base_crawler import BaseCrawler

class MyCustomCrawler(BaseCrawler):
    async def crawl(self):
        # Implement your logic
        async for page in self.discover_pages():
            await self.process_page(page)
    
    async def process_page(self, page):
        # Custom processing logic
        if "special-content" in page.url:
            await self.handle_special(page)
```

2. Register in `main.py`:

```python
from .crawlers.my_crawler import MyCustomCrawler

CRAWLER_REGISTRY.register("my_crawler", MyCustomCrawler)
```

## Building detection strategies

```python
# detectors/strategies/my_detector.py
import re
from typing import Dict, Any
from src.core.site_type import SiteType

class MyDetector(DetectionStrategy):
    PRIORITY = 500  # Higher runs first
    
    async def detect(self, url: str, response) -> bool:
        return "X-Powered-By: MyTech" in response.headers
```