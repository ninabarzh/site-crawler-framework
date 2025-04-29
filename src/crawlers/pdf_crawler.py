"""
Specialized crawler for PDF documents.
"""

from typing import Dict, Any
import io
from urllib.parse import urlparse
from pathlib import Path

from src.core.base_crawler import BaseCrawler
from src.core.site_type import SiteType
from src.core.content_handler import ContentHandler
from src.modules.content_extractor import ContentExtractor


class PDFCrawler(BaseCrawler):
    """Crawler specialized for handling PDF documents."""

    def get_site_type(self) -> SiteType:
        """Get the site type this crawler handles.

        Returns:
            SiteType.PDF enum value
        """
        return SiteType.PDF

    async def crawl(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """
        Process a PDF document.

        Args:
            url: URL of the PDF document
            depth: Current crawl depth (ignored for PDFs)

        Returns:
            Dictionary containing processed PDF information with keys:
            - url: Original URL
            - status: HTTP status code
            - content_type: Detected content type
            - saved_path: Where file was saved (if saved)
            - metadata: Extracted metadata
            - extracted_text: First 1000 chars of text
        """
        if depth > 0:  # PDFs don't have links to follow
            return {}

        response = await self.fetch(url)
        if not response or 'application/pdf' not in response.get('content_type', ''):
            return {}

        # Extract text from PDF using ContentExtractor
        try:
            pdf_text = ContentExtractor.extract_text_from_pdf(
                source=io.BytesIO(response['content'])
            )
        except Exception as e:
            self.logger.error(f"PDF text extraction failed for {url}: {str(e)}")
            pdf_text = None

        # Process and save content
        content_handler = ContentHandler(self.config)
        output_dir = Path(self.config['storage']['output_dir']) / urlparse(url).netloc
        result = content_handler.process_content(response, output_dir)

        # Add extracted text to results if successful
        if pdf_text:
            result['extracted_text'] = pdf_text[:1000]  # Store first 1000 chars
        else:
            result['extracted_text'] = None

        return result
