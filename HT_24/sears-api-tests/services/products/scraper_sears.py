from dataclasses import asdict
from dataclasses import dataclass
from sqlite3 import IntegrityError
from time import sleep
from urllib.parse import urljoin

import requests
from loguru import logger
from requests import JSONDecodeError

from apps.products.models import Category
from apps.products.models import Product

logger.add('logs/errors_log.json',
           filter=lambda record: record["level"].name == "ERROR",
           format='{time} {level} {message}',
           level='DEBUG',
           rotation='10 MB',
           compression='zip',
           serialize=True)


@dataclass
class SearsData:
    product_id: str
    name: str
    brand: str
    short_description: str
    category: Category
    image_url: str
    base_price: float
    final_price: float
    savings_price: float
    url: str


class ScraperSears:
    HEADERS = {
        'authority': 'www.sears.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': 'SEARS',
        'content-type': 'application/json',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }

    MAIN_URL = 'https://www.sears.com'

    def __init__(self, product_ids):
        self.product_ids = self.parse_user_ids(product_ids)

    def scrape(self, item_id):
        response = requests.get(
            f'https://www.sears.com/api/sal/v3/products/details/{self.__get_clean_id(item_id)}?'
            f'storeName=Sears&memberStatus=G&zipCode=10101',
            headers=self.HEADERS)

        product = response.json()

        detail = product.get('productDetail').get('softhardProductdetails')[0]
        return SearsData(
            product_id=detail.get("identity").get("sSin"),
            name=detail.get('descriptionName'),
            brand=detail.get('brandName'),
            short_description=detail.get('shortDescription'),
            image_url=detail.get('mainImageUrl'),
            base_price=self.__get_price(detail.get('price').get('regularPrice')),
            final_price=self.__get_price(detail.get('price').get('finalPrice')),
            savings_price=self.__get_price(detail.get('price').get('savings')),
            url=urljoin(self.MAIN_URL, detail.get('seoUrl')),
            category=self.get_category(detail),
        )

    @staticmethod
    def __get_price(data_price: str) -> float:
        if data_price is None:
            return 0.0

        price = data_price.strip().replace('$', '').split(' - ')
        if len(price) == 2:
            _, price = price
        else:
            price = price[0]

        return float(price)

    @staticmethod
    def __get_clean_id(input_id: str) -> str:
        if input_id.startswith('p-'):
            return input_id[2:]
        return input_id

    @staticmethod
    def get_category(response):
        cat_name = response.get('hierarchies').get('specificHierarchy')[-2].get('name')
        obj, _ = Category.objects.update_or_create(name=cat_name)
        return obj

    @staticmethod
    def parse_user_ids(product_ids: str) -> list[str]:
        replacements = [';', ',', ' ', '\n\n', '\r']

        for char in replacements:
            if char in product_ids:
                product_ids = product_ids.replace(char, '\n').strip()
        return [prod_id.strip() for prod_id in product_ids.split('\n') if prod_id]

    def scraper_process(self, prod_id):
        try:
            product = self.scrape(prod_id)
            if product:
                Product.objects.update_or_create(product_id=product.product_id, defaults=asdict(product))
                logger.info(f'scraped "{prod_id}" - OK')
        except AttributeError as e:
            logger.error(e)
        except IntegrityError as e:
            logger.error(e)

    def start(self):
        timer = 60
        for prod_id in self.product_ids:
            try:
                self.scraper_process(prod_id)
            except JSONDecodeError:
                logger.info(f'Sleeping {timer} seconds {prod_id}.')
                sleep(timer)
                self.scraper_process(prod_id)
            except Exception as e:
                logger.error(e)

        logger.info('Finished scraping')
