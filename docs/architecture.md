# Architectural overview

```mermaid
graph TD
    A[Config Loader] --> B[Crawler Manager]
    B --> C[Detection System]
    C --> D[Sphinx Crawler]
    C --> E[PDF Handler]
    C --> F[Custom Crawlers]
    B --> G[Content Pipeline]
    G --> H[Storage Backends]
```

## Key components

Core engine:

- Async event loop
- Rate limiting
- Retry logic

Detection flow:

- URL pre-processing
- Header inspection
- Content sniffing
- Fallback to generic

Extension points:

- Crawler registration
- Detection strategies
- Content processors
- Storage adapters
