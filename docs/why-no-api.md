# Design Philosophy

## Configuration-first approach

- All behaviour controlled via YAML/JSON
- Zero code required for basic usage
- Environment-aware templating

## Extension model

1. **Discovery**:
   - Automatic crawler detection
   - Priority-based strategy selection

2. **Composition**:
   - Mixins for common functionality
   - Decorators for cross-cutting concerns

3. **Conventions**:
   - Standard directory layout
   - Automatic registration
   - Config-driven activation

## Runtime integration

```python
# Instead of API calls:
# config/sites_to_crawl.yaml
sites:
  - url: "{{API_ENDPOINT}}"
    type: "api_crawler"
    options:
      format: "json"
      auth: "{{API_KEY}}"
```