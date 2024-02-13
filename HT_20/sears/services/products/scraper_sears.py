from dataclasses import dataclass
from urllib.parse import urljoin

import requests

from apps.products.models import Category


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
