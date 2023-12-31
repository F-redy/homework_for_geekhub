if __name__ == "__main__":
    import sys
    from pathlib import Path

    current_dir = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(current_dir))

from dataclasses import asdict

from time import sleep

import django

django.setup()

from scraper_sears import ScraperSears

from apps.products.models import Product


def get_product_ids():
    if len(sys.argv) > 1:
        for id_ in sys.argv[1].split('\r'):
            if id_.strip():
                yield id_.strip('\n')


def start():
    scraper = ScraperSears()

    for item in get_product_ids():
        try:
            product = scraper.scrape(item)
            print(f'scraped {item} - OK')
            Product.objects.update_or_create(**asdict(product))

        except Exception as e:
            print(f'Error  with "{item}": {e}')

        sleep(20)
    print('Finished scraping')


if __name__ == '__main__':
    start()
