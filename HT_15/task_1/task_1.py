# 1. Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID категорії
# із сайту https://www.sears.com і буде збирати всі товари із цієї категорії, збирати по ним всі можливі дані
# (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх
# у CSV файл (наприклад, якщо категорія має ID 12345, то файл буде називатись 12345_products.csv)


import csv
import http
import os
from time import sleep
from urllib.parse import urljoin

import requests


class SearsScraper:
    FIELD_NAMES = [
        'Brand Name', 'Product Name', 'Base Price', 'Final Price', 'Savings Price', 'Category', 'Rating', 'URL'
    ]
    BASE_URL = 'https://www.sears.com'
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

    def __init__(self, catalog_id: int):
        self.catalog_id = catalog_id
        self.path_to_save = self.get_path_to_save()
        self.start_index = 1
        self.end_index = 48
        self.timer_sleep = 3
        self.meta_count = None
        self.total_products = 0

    def get_path_to_save(self):
        return f'{os.path.join("products", str(self.catalog_id))}_products.csv'

    def get_path_to_url_product(self, url_product: str):
        return urljoin(self.BASE_URL, url_product)

    def write_to_csv(self, products):
        with open(f'{self.path_to_save}', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            writer.writeheader()
            for product in products:
                writer.writerow(product)

    def make_api_request(self, start_index, end_index):
        response = requests.get(f'https://www.sears.com/api/sal/v3/products/search?'
                                f'startIndex={start_index}&'
                                f'endIndex={end_index}&'
                                f'searchType=category&catalogId=12605&'
                                f'store=Sears&storeId=10153&zipCode=10101&bratRedirectInd=true&'
                                f'catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&'
                                f'includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&'
                                f'sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad=true&'
                                f'slimResponseInd=true&catGroupPath=Appliances%7CSpecialty%20Laundry&'
                                f'catGroupId={self.catalog_id}',
                                headers=self.HEADERS)

        return response

    def process_data_and_save(self, data):
        products = []
        try:
            for product in data['items']:
                products.append({
                    'Product Name': product.get('brandName'),
                    'Brand Name': product.get('name'),
                    'Base Price': product.get('price', dict()).get('regularPriceDisplay'),
                    'Final Price': product.get('price', dict()).get('finalPriceDisplay'),
                    'Savings Price': product.get('price', dict()).get('savings'),
                    'Category': product.get('category'),
                    'Rating': product.get('additionalAttributes', dict()).get('rating'),
                    'URL': self.get_path_to_url_product(product.get('additionalAttributes', dict()).get('seoUrl')),
                })
        except IndexError:
            pass
        if products:
            self.write_to_csv(products)

    def scrape(self):
        start_index = self.start_index
        end_index = self.end_index

        while True:

            response = self.make_api_request(start_index, end_index)

            if response.status_code == http.HTTPStatus.OK:

                data = response.json()

                if self.meta_count is None:
                    self.meta_count = int(data['metadata']['count'])

                self.process_data_and_save(data)

                start_index += len(data['items'])
                end_index += len(data['items'])
                self.total_products += len(data['items'])

                if self.meta_count < end_index:
                    print('The program is completed.'
                          f'\nTotal scraper received {self.total_products} from {self.meta_count}.')
                    break

                print(f'Sleeping for {self.timer_sleep} seconds...')
                sleep(self.timer_sleep)

            elif response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
                print('The limit of IP addresses for the request has been exceeded. Sleeping for 1 minute...')
                sleep(60)

            else:
                print(f'Program finished with an error. {response.status_code}'
                      f'\nA total of {self.total_products} scraper out of {self.meta_count} were received.')
                break


if __name__ == '__main__':
    # scraper = SearsScraper(1020198) # Отрабатывает нормально
    scraper = SearsScraper(1025184)  # Слишком много товаров, после 1200 ++ сервер блокирует запрос
    scraper.scrape()
