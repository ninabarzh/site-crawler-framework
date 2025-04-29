"""
Main application entry point with all warnings and unused variables resolved.
"""

import asyncio
import signal
from pathlib import Path
from typing import Optional, Any, List, cast
from src.core.models import CrawlerConfig, SiteConfig
from src.core.exceptions import ConfigError
from src.crawlers.manager import CrawlerManager
from src.crawlers.resolver import CrawlerResolver
from src.modules.config_loader import load_config
from src.modules.logger import setup_logging, get_logger

async def main() -> None:
    """Main application workflow with all issues resolved."""
    manager: Optional[CrawlerManager] = None
    logger = get_logger('main', {})

    try:
        # 1. Configuration loading
        config_path = Path('config/crawler_config.yaml')
        sites_path = Path('config/sites_to_crawl.yaml')

        config = CrawlerConfig(**load_config(str(config_path)))
        sites = [SiteConfig(**site) for site in load_config(str(sites_path)).get('sites', [])]

        if not sites:
            raise ConfigError("No valid sites configured")

        # 2. System initialization
        setup_logging(config.logging)
        logger = get_logger('main', cast(dict[str, Any], config.logging))
        manager = CrawlerManager(config=config)
        resolver = CrawlerResolver(config=config.model_dump())

        # 3. Signal handling with direct signal.signal() approach
        def _create_signal_callback() -> Any:
            """Creates a properly typed signal callback."""
            def handler(signum: int, _frame: Any) -> None:
                nonlocal manager
                if manager:
                    logger.warning(f"Received signal {signum}")
                    asyncio.create_task(manager.shutdown())
            return handler

        # Register signals directly - no loop.add_signal_handler() needed
        signal.signal(signal.SIGINT, _create_signal_callback())
        signal.signal(signal.SIGTERM, _create_signal_callback())

        # 4. Main execution
        logger.info(f"Starting crawler with {len(sites)} sites")
        while manager and not manager.shutdown_event.is_set():
            tasks: List[asyncio.Task[Any]] = []

            for site in sites:
                try:
                    crawler_class = await resolver.resolve(site)
                    task = asyncio.create_task(manager.run_crawler(crawler_class, site))
                    tasks.append(task)
                except Exception as e:
                    logger.error(f"Failed on {site.url}: {e!r}")

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

            if manager and not manager.shutdown_event.is_set():
                await asyncio.sleep(config.timeout)

    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        if manager:
            await manager.shutdown()
        logger.info("Application shutdown complete")

if __name__ == '__main__':
    asyncio.run(main())