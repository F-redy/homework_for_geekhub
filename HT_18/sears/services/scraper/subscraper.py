if __name__ == "__main__":
    import sys
    from pathlib import Path

    current_dir = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(current_dir))

from dataclasses import asdict
from time import sleep

import django
from loguru import logger

django.setup()

from apps.products.models import Product
from scraper_sears import ScraperSears

logger.add('logs/errors_log.json',
           filter=lambda record: record["level"].name == "ERROR",
           format='{time} {level} {message}',
           level='DEBUG',
           rotation='10 MB',
           compression='zip',
           serialize=True)


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
            if product:
                Product.objects.update_or_create(**asdict(product))
                logger.info(f'scraped "{item}" - OK')

        except AttributeError:
            logger.error(f'Invalid id "{item}".')

        sleep(20)
    logger.info('Finished scraping')


if __name__ == '__main__':
    start()
