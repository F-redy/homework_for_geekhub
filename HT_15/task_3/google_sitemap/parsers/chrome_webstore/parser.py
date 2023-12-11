from bs4 import BeautifulSoup
from google_sitemap.parsers.chrome_webstore.dataclasses import LocationItem  # isort:split
from google_sitemap.parsers.chrome_webstore.dataclasses import LocationItemData  # isort:split
from google_sitemap.parsers.chrome_webstore.dataclasses import SitemapItem  # isort:split


class GoogleChromeParser:
    BASE_URL = 'https://chrome.google.com'

    @staticmethod
    def parse_sitemap(response_test: str) -> list[SitemapItem]:
        soup = BeautifulSoup(response_test, 'xml')
        return [
            SitemapItem(
                location=loc.text.strip()
            )
            for loc in soup.select('sitemap > loc')
        ]

    @staticmethod
    def parse_location(response_test: str) -> list[LocationItem]:
        soup = BeautifulSoup(response_test, 'xml')
        return [
            LocationItem(url=location.text.strip())
            for location in soup.select('url > loc')
            if "detail" in location.text
        ]

    @staticmethod
    def parse_location_data(response) -> LocationItemData:
        extension_id = response.css('[property="og:url"]::attr(content)').get().split('/').pop()
        title = response.css('[property="og:title"]::attr(content)').get()
        description = response.css('[property="og:description"]::attr(content)').get()

        return LocationItemData(
            extension_id=extension_id,
            title=title,
            description=description
        )
