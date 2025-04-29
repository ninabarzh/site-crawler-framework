# Site Crawler Framework

```text

          _____
         /     \ 
        | () () |   __
         \  ^  /  /  \
          |||||  /    \
          ||||| |      |
          |||||  \____/
         /|/\|\
        / /  \ \
       / /    \ \
      /_/      \_\

[Debugging session in progress...]
```

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
[![Async Ready](https://img.shields.io/badge/asyncio-ready-green.svg)](https://docs.python.org/3/library/asyncio.html)

A modular, extensible web crawler framework with automatic site detection and specialized crawling strategies.

## Features

- **Pluggable Architecture** - Add new crawlers for different site types with minimal code
- **Smart Detection** - Auto-detects site technology (Flask, Sphinx, WordPress, etc.)
- **Content-Aware** - Specialized handlers for PDFs, APIs, and dynamic content
- **Async First** - Built with asyncio for high-performance crawling
- **Configuration Driven** - YAML/JSON configuration support
- **Extensible** - Easy to add new detection strategies and crawlers

## Installation

```bash
# Install from PyPI
pip install site-crawler-framework

# Or install from source
git clone https://github.com/yourusername/site-crawler-framework.git
cd site-crawler-framework
pip install .

# For development
pip install -e .[dev,test]
```

## Quick start

Configure your crawler:

```yaml
# config/crawler_config.yaml
timeout: 30
max_depth: 3
user_agent: "MyCrawler/1.0"
```

Add sites to crawl:

```yaml
# config/sites_to_crawl.yaml
sites:
  - url: "https://example.com"
    type: "auto"
  - url: "https://wordpress.example.com"
    type: "wordpress"
```

Run:

```bash
python -m site_crawler_framework
```

## Extending the framework

To add a new crawler:

1. Create a crawler class in crawlers/:

```python
from .base import BaseCrawler

class MyCustomCrawler(BaseCrawler):
    async def crawl(self):
        # Your custom crawling logic
```
    
2. (Optional) Create a detection strategy in detectors/strategies/
3. Register your crawler in main.py:

```python
CRAWLER_REGISTRY.register("my_crawler", MyCustomCrawler)
```

## Documentation (under construction)

See the docs/ directory for:

- Configuration reference
- Extension guide
- API documentation
- Example crawlers

## Debugging Quick Start
    
1. Configure:

```yaml
# config/frustration_levels.yaml
parameter_warnings: ignore
type_checker_arguments: surrender
```
    
2. Run:

```bash
python -c "import asyncio; from site_crawler_framework import main; asyncio.run(main.run())"
# (Yes, it's supposed to look like that)
```

## Debugging tips

When all else fails:

- Make coffee
- Check indentation
- Blame the type checker
- Repeat

## License

This project is Unlicensed - do whatever you want with it!