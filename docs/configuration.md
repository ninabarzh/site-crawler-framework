# Configuration reference

## Core structure

```yaml
# config/crawler_config.yaml
timeout: 30               # Global timeout in seconds
max_depth: 3              # Maximum crawl depth
user_agent: "MyCrawler/1.0"
concurrency: 5            # Max concurrent requests
logging:
  level: "INFO"
  file: "crawler.log"
```

## Site-specific options

```yaml
# config/sites_to_crawl.yaml
sites:
  - url: "https://example.com"
    type: "auto"          # Auto-detection
    options:
      depth: 2            # Override global max_depth
      exclude: ["*.pdf"]  # Exclude PDFs
  
  - url: "https://wp.example.com"
    type: "wordpress"     # Force specific handler
    auth:
      username: "admin"
      password: "{{WP_PASSWORD}}" # Env variable
```

## Environment variables

| Variable	           | Purpose                      |
|---------------------|------------------------------|
| CRAWLER_TIMEOUT	    | Overrides default timeout    |
| CRAWLER_MAX_DEPTH	  | Sets maximum traversal depth |
| CRAWLER_USER_AGENT	 | Custom user agent string     |
