# Site Crawler Framework (being developed)

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

## Documentation approach

Since this is a configuration-driven framework rather than a traditional library with public API, documentation focuses on usage patterns and extension points:

### Configuration reference

[docs/configuration.md](docs/configuration.md) covers:

- Core YAML structure
- Available settings
- Site-specific options
- Environment variables

### Extension guide

[docs/extending.md](docs/extending.md) explains 

1. How to add new crawlers:
    - Inherit from BaseCrawler
    - Implement required methods
    - Register in CRAWLER_REGISTRY
2. Creating detection strategies:
    - Pattern matching rules
    - Priority system
    - Testing new detectors

### Architectural overview

[docs/architecture.md](docs/architecture.md) describes:

- Core component diagram
- Data flow
- Async operation model
- Error handling approach

### Why No Formal API?

[docs/why-no-api.md](docs/why-no-api.md) explains the design philosopy, if you can call it that. The framework operates through:

1. Configuration files as primary interface
2. Convention-over-codebase extension model
3. Runtime composition rather than import-time integration

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