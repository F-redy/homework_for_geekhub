from typing import Any
from urllib.parse import urljoin

import scrapy
from google_sitemap.items import GoogleSitemapItem
from google_sitemap.parsers.chrome_webstore.parser import GoogleChromeParser
from scrapy import Request
from scrapy.http import Response


class GoogleCrawlSpider(scrapy.Spider):
    parser = GoogleChromeParser()

    name = 'google_crawl'
    start_urls = [urljoin(parser.BASE_URL, '/webstore/sitemap')]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        results = self.parser.parse_sitemap(response.text)
        for url in results:
            yield Request(
                url=url.location,
                callback=self.parse_location
            )

    def parse_location(self, response: Response):
        results = self.parser.parse_location(response.text)

        for location in results:
            yield Request(
                url=location.url,
                callback=self.parse_location_data
            )

    def parse_location_data(self, response: Response):
        result = self.parser.parse_location_data(response)

        item = GoogleSitemapItem(
            extension_id=result.extension_id,
            title=result.title,
            description=result.description
        )
        yield item
