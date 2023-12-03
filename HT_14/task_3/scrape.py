import csv
import http
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as BS


class QuotesScraper:
    BASE_URL = 'https://quotes.toscrape.com/'
    FIELDS_NAMES = ['Quote', 'Author', 'Born Date', 'Born Location', 'Description', 'Tags']
    FILE_TO_SAVE = 'quotes.csv'

    @staticmethod
    def get_quotes_from_page(url):
        response = requests.get(url)
        if response.status_code == http.HTTPStatus.OK:
            soup = BS(response.content, 'html.parser')
            return soup.find_all('div', class_='quote')
        return []

    @staticmethod
    def get_next_page_url(url: str) -> str | None:
        response = requests.get(url)
        if response.status_code == http.HTTPStatus.OK:
            soup = BS(response.content, 'html.parser')
            next_page = soup.find('li', class_='next')
            if next_page:
                return urljoin(url, next_page.find('a')['href'])
        return None

    @staticmethod
    def parse_author(author_url: str) -> tuple[str, str, str] | None:
        author_page = requests.get(author_url)
        if author_page.status_code == http.HTTPStatus.OK:
            author_soup = BS(author_page.content, 'lxml')

            born_date = author_soup.find('span', class_='author-born-date').text
            born_location = author_soup.find('span', class_='author-born-location').text
            description = author_soup.find('div',
                                           class_='author-description').text.replace('\n', '').strip()

            return born_date, born_location, description

    def get_author_info(self, quote: BS, authors: dict[str: tuple]):
        author = quote.find('small', class_='author')
        author_name = author.text

        print(f'\t\tGetting author information: {author_name}')
        if author_name in authors:
            born_date, born_location, description = authors[author_name]
        else:
            author_url = urljoin(self.BASE_URL, author.find_next_sibling('a')['href'])
            born_date, born_location, description = self.parse_author(author_url)
            authors[author_name] = born_date, born_location, description

        return author_name, born_date, born_location, description, authors

    def get_all_quotes(self) -> list[dict]:
        quotes_list = []
        url = self.BASE_URL
        page_number = 1
        authors = {}

        while url:
            print(f'Getting data from {page_number} page:')
            quotes = self.get_quotes_from_page(url)

            for quote in quotes:
                text = quote.find('span', class_='text').text
                tags = [tag.text for tag in quote.find_all('a', class_='tag')]

                author_name, born_date, born_location, description, authors = self.get_author_info(quote, authors)

                quotes_list.append({
                    'Quote': text,
                    'Author': author_name,
                    'Born Date': born_date,
                    'Born Location': born_location,
                    'Description': description,
                    'Tags': ', '.join(tags),
                })

            url = self.get_next_page_url(url)
            page_number += bool(url)

        return quotes_list

    def write_quotes_to_csv(self, quotes: list[dict]) -> None:
        print(f'Writing data to {self.FILE_TO_SAVE}')
        with open(self.FILE_TO_SAVE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.FIELDS_NAMES)
            writer.writeheader()
            for quote in quotes:
                writer.writerow(quote)
        print('Finished writing data.')

    def start(self) -> None:
        quotes_list = self.get_all_quotes()
        self.write_quotes_to_csv(quotes_list)


if __name__ == '__main__':
    QuotesScraper().start()
