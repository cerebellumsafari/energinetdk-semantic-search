import os
import re
from typing import Any
from uuid import uuid4
from bs4 import BeautifulSoup
from scrapy import Spider
from scrapy.http import Request, Response

from .config import DATA_FOLDER


class EnerginetSpider(Spider):
    """
    A spider that crawls the Energinet.dk website and downloads all PDF files.
    """
    name = 'energinetdk'
    allowed_domains = ['energinet.dk']
    start_urls = ['https://www.energinet.dk']

    def parse(self, response: Response, **kwargs: Any):
        """
        Parse a response from the spider.
        """
        if 'text/html' in response.headers.get('Content-Type', '').decode():
            soup = BeautifulSoup(response.text, 'html.parser')
            text_whitespaces_stripped = re.sub(r'\s+', ' ', soup.text)

            yield {
                'type': 'website-link',
                'source_url': response.url,
                'title': soup.title.string if soup.title else None,
                'content': text_whitespaces_stripped,
            }

            # Extract all links on the page and follow them
            for href in response.css('a::attr(href)').getall():
                url = response.urljoin(href)

                if url.endswith('.pdf'):
                    file_id = str(uuid4())
                    original_filename = url.split('/')[-1]
                    original_name, ext = os.path.splitext(original_filename)
                    filename = f'{original_name}-{file_id}{ext}'

                    # Save metadata about the PDF
                    # Used when processing the crawled data later on
                    yield {
                        'type': 'pdf-file',
                        'source_url': response.url,
                        'file_url': url,
                        'filename': filename,
                    }

                    # Download the PDF
                    yield Request(
                        url=url,
                        callback=self.save_pdf,
                        meta={'filename': filename},
                    )
                elif url.startswith('https://'):
                    # 'https://' to ignore '#', 'mailto://' etc.
                    yield response.follow(href, self.parse)

    def save_pdf(self, response: Response, **kwargs: Any):
        """
        Save a PDF file.
        """
        folder = os.path.join(DATA_FOLDER, 'files')
        filepath = os.path.join(folder, response.meta['filename'])

        os.makedirs(folder, exist_ok=True)

        with open(filepath, 'wb') as file:
            file.write(response.body)
