"""
Crawler manager with proper shutdown handling.
"""

import asyncio
from typing import Set
from src.core.models import CrawlerConfig, SiteConfig
from src.modules.logger import get_logger

class CrawlerManager:
    def __init__(self, config: CrawlerConfig):
        self.tasks: Set[asyncio.Task] = set()
        self.shutdown_event = asyncio.Event()
        self.config = config
        self.logger = get_logger('manager', config.logging)
        self._shutdown_lock = asyncio.Lock()

    async def run_crawler(self, crawler_class: type, site_config: SiteConfig) -> None:
        """Run an individual crawler instance with shutdown awareness"""
        if self.shutdown_event.is_set():
            return

        try:
            async with crawler_class(self.config.model_dump(), site_config.model_dump()) as crawler:
                task = asyncio.create_task(
                    self._run_crawler_safely(crawler, site_config.url),
                    name=f"crawl-{site_config.url}"
                )
                self.tasks.add(task)
                await task
        except Exception as e:
            self.logger.error(f"Crawler error: {str(e)}")
            raise
        finally:
            self.tasks.discard(task)

    async def _run_crawler_safely(self, crawler, url: str) -> None:
        """Wrapper for safe crawler execution"""
        try:
            if not self.shutdown_event.is_set():
                await crawler.crawl(url)
        except asyncio.CancelledError:
            self.logger.warning(f"Crawler for {url} cancelled")
            await crawler.close()  # Ensure proper cleanup
            raise
        except Exception as e:
            self.logger.error(f"Crawler failed for {url}: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Graceful shutdown with lock to prevent multiple calls"""
        async with self._shutdown_lock:
            if self.shutdown_event.is_set():
                return

            self.logger.info("Initiating graceful shutdown...")
            self.shutdown_event.set()

            # Cancel all running tasks with timeout
            if self.tasks:
                self.logger.info(f"Cancelling {len(self.tasks)} active crawlers...")
                for task in self.tasks:
                    task.cancel()

                await asyncio.wait(
                    self.tasks,
                    timeout=self.config.timeout,
                    return_when=asyncio.ALL_COMPLETED
                )

            self.logger.info("Shutdown complete")
