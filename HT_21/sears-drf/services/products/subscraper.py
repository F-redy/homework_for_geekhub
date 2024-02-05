from sqlite3 import IntegrityError

if __name__ == "__main__":
    import sys
    from pathlib import Path

    current_dir = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(current_dir))

from dataclasses import asdict
from time import sleep

import django
from loguru import logger
from requests import JSONDecodeError

django.setup()

from scraper_sears import ScraperSears

from apps.products.models import Product

logger.add('logs/errors_log.json',
           filter=lambda record: record["level"].name == "ERROR",
           format='{time} {level} {message}',
           level='DEBUG',
           rotation='10 MB',
           compression='zip',
           serialize=True)


def parse_response(response: str) -> list[str]:
    replacements = [';', ',', ' ', '\n\n', '\r']

    for char in replacements:
        if char in response:
            response = response.replace(char, '\n').strip()
    return response.split('\n')


def get_product_ids():
    if len(sys.argv) > 1:
        response = parse_response(sys.argv[1])

        for id_ in response:
            if id_.strip():
                yield id_.strip('\n').strip()


def scraper_process(item):
    try:
        scraper = ScraperSears()
        product = scraper.scrape(item)

        if product:
            Product.objects.update_or_create(product_id=product.product_id, defaults=asdict(product))
            logger.info(f'scraped "{item}" - OK')
    except AttributeError as e:
        logger.error(e)
    except IntegrityError as e:
        logger.error(e)


def start():
    timer = 60
    for item in get_product_ids():
        try:
            scraper_process(item)
        except JSONDecodeError:
            logger.info(f'Sleeping {timer} seconds {item}.')
            sleep(timer)
            scraper_process(item)
        except Exception as e:
            logger.error(e)

    logger.info('Finished scraping')


if __name__ == '__main__':
    start()
